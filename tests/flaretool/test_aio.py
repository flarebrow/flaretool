"""非同期版（aio）ラッパーのテスト。

同期テストと同じシーム（flaretool.common.requests.request）をモックし、
非同期ラッパーが実際の同期ロジックをイベントループ外で駆動することを検証する。
"""

import asyncio
import warnings
from datetime import datetime
from unittest.mock import patch

import pytest

import flaretool
from flaretool.ddns import AsyncDdnsService, DdnsService
from flaretool.ddns.models import DdnsInfo
from flaretool.errors import AuthenticationError
from flaretool.nettool import aio as nettool_aio
from flaretool.nettool.models import PunyDomainInfo
from flaretool.shorturl import AsyncShortUrlService, ShortUrlService
from flaretool.shorturl.models import ShortUrlInfo

SHORTURL_RESULT = {
    "id": 1,
    "url": "https://example.com",
    "title": "Example",
    "code": "abcd",
    "owner": "owner",
    "is_active": True,
    "is_eternal": False,
    "limited_at": None,
    "created_at": "2023-06-10T12:00:00",
    "updated_at": "2023-06-10T12:00:00",
    "short_url": "https://example.com/abcd",
    "qr_url": "https://example.com/abcd/qr",
}

DDNS_RESULT = {
    "result": 200,
    "status": "success",
    "currentIp": "192.168.0.99",
    "updateIp": "192.168.0.100",
    "domain": "example.○○○.○○",
}


@pytest.fixture(autouse=True)
def api_key():
    original = flaretool.api_key
    flaretool.api_key = "API_KEY"
    yield
    flaretool.api_key = original


def _mock_response(mock_request, payload, status_code=200):
    mock_request.return_value.status_code = status_code
    mock_request.return_value.json.return_value = payload


# ---------------------------------------------------------------------------
# shorturl
# ---------------------------------------------------------------------------


async def test_async_shorturl_create_sends_payload():
    with patch("flaretool.common.requests.request") as mock_request:
        _mock_response(mock_request, {"response": 200, "result": SHORTURL_RESULT})

        service = AsyncShortUrlService()
        result = await service.create(
            "https://example.com", is_eternal=False, is_active=True
        )

        assert isinstance(result, ShortUrlInfo)
        assert result.id == 1
        assert result.url == "https://example.com"
        assert result.code == "abcd"
        assert result.created_at == datetime.fromisoformat("2023-06-10T12:00:00")

        args, kwargs = mock_request.call_args
        assert args[0] == "post"
        assert kwargs["json"] == {
            "url": "https://example.com",
            "is_eternal": False,
            "is_active": True,
        }
        assert kwargs["auth_enabled"] is True


async def test_async_shorturl_get_with_context_manager():
    with patch("flaretool.common.requests.request") as mock_request:
        _mock_response(
            mock_request,
            {
                "response": 200,
                "result": [SHORTURL_RESULT, {**SHORTURL_RESULT, "id": 2}],
            },
        )

        async with AsyncShortUrlService() as service:
            all_infos = await service.get()
            one_info = await service.get(2)

        assert [info.id for info in all_infos] == [1, 2]
        assert [info.id for info in one_info] == [2]
        assert all(isinstance(info, ShortUrlInfo) for info in all_infos)


async def test_async_shorturl_accepts_injected_sync_service():
    sync_service = ShortUrlService()
    service = AsyncShortUrlService(_service=sync_service)
    assert service._sync is sync_service


# ---------------------------------------------------------------------------
# ddns
# ---------------------------------------------------------------------------


async def test_async_ddns_update_ddns():
    with patch("flaretool.common.requests.request") as mock_request:
        _mock_response(mock_request, DDNS_RESULT)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            async with AsyncDdnsService() as service:
                info = await service.update_ddns("example", "192.168.0.100")

        assert isinstance(info, DdnsInfo)
        assert info.result == 200
        assert info.status == "success"
        assert info.updateIp == "192.168.0.100"
        assert info.domain == "example.○○○.○○"
        mock_request.assert_called_once_with(
            "post",
            "https://api.flarebrow.com/v2/ddns",
            params={},
            data={"host": "example", "ip": "192.168.0.100"},
            auth_enabled=True,
        )


async def test_async_ddns_accepts_injected_sync_service():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sync_service = DdnsService()
    service = AsyncDdnsService(_service=sync_service)
    assert service._sync is sync_service


# ---------------------------------------------------------------------------
# nettool.aio
# ---------------------------------------------------------------------------


async def test_async_nettool_pure_functions_no_mock():
    # get_robots_txt_url / is_ip_in_allowed_networks はローカル演算のみ
    url = await nettool_aio.get_robots_txt_url("https://example.com/page?q=1")
    assert url == "https://example.com/robots.txt"

    assert await nettool_aio.is_ip_in_allowed_networks(
        "192.168.1.10", ["192.168.1.0/24"]
    )
    assert not await nettool_aio.is_ip_in_allowed_networks(
        "10.0.0.1", ["192.168.1.0/24"]
    )


async def test_async_nettool_get_puny_code():
    # get_puny_code はローカルidna変換ではなくAPI呼び出しのためモックが必要
    with patch("flaretool.common.requests.request") as mock_request:
        _mock_response(
            mock_request,
            {
                "originalvalue": "日本語.jp",
                "encodevalue": "xn--wgv71a119e.jp",
                "decodevalue": "日本語.jp",
            },
        )

        result = await nettool_aio.get_puny_code("日本語.jp")

        assert isinstance(result, PunyDomainInfo)
        assert result.encodevalue == "xn--wgv71a119e.jp"
        args, _ = mock_request.call_args
        assert args[0].lower() == "get"
        assert args[1].endswith("/puny/日本語.jp")


# ---------------------------------------------------------------------------
# 並行実行・エラー伝播
# ---------------------------------------------------------------------------


async def test_async_concurrent_calls_with_gather():
    with patch("flaretool.common.requests.request") as mock_request:
        _mock_response(mock_request, {"response": 200, "result": [SHORTURL_RESULT]})

        async with AsyncShortUrlService() as service:
            results = await asyncio.gather(
                service.get(),
                service.get(),
                service.get(1),
            )

        assert len(results) == 3
        assert all(infos[0].id == 1 for infos in results)
        assert mock_request.call_count == 3


async def test_async_shorturl_missing_api_key_raises():
    flaretool.api_key = None
    with pytest.raises(AuthenticationError):
        AsyncShortUrlService()


async def test_async_ddns_missing_api_key_raises():
    flaretool.api_key = None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with pytest.raises(AuthenticationError):
            AsyncDdnsService()

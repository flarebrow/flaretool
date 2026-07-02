"""ネットワークツールの非同期版関数群。

:mod:`flaretool.nettool` の公開関数と同名の ``async def`` 版を提供します。
各関数は ``asyncio.to_thread`` で同期版をワーカースレッドに委譲するため、
イベントループをブロックせずに利用できます。

Note:
    同期版と名前が衝突するため、これらの関数は ``flaretool.nettool``
    パッケージ直下には再エクスポートされません。次のように本モジュールを
    明示的にインポートして利用してください::

        from flaretool.nettool import aio
        info = await aio.get_global_ipaddr_info()

        # または関数を直接インポート
        from flaretool.nettool.aio import lookup_ip
        ip = await lookup_ip("example.com")
"""

import asyncio

from flaretool.constants import Country
from flaretool.nettool import common as _sync
from flaretool.nettool.models import IpInfo, PunyDomainInfo

__all__ = [
    "lookup_domain",
    "lookup_ip",
    "get_global_ipaddr_info",
    "domain_exists",
    "is_ip_in_allowed_networks",
    "get_japanip_list",
    "is_country_ip",
    "get_country_ip_list",
    "is_japan_ip",
    "get_puny_code",
    "get_adhost",
    "get_robots_txt_url",
    "is_scraping_allowed",
]


async def get_global_ipaddr_info(addr: str | None = None) -> IpInfo:
    """非同期版: 指定されたグローバルIPアドレスの情報を取得する関数"""
    return await asyncio.to_thread(_sync.get_global_ipaddr_info, addr)


async def lookup_ip(domain: str) -> str | None:
    """非同期版: 指定されたドメイン名からIPアドレスを取得する関数"""
    return await asyncio.to_thread(_sync.lookup_ip, domain)


async def lookup_domain(ip: str) -> str | None:
    """非同期版: 指定されたIPアドレスからドメイン名を取得する関数"""
    return await asyncio.to_thread(_sync.lookup_domain, ip)


async def is_ip_in_allowed_networks(ipaddr: str, allow_networks: list[str]) -> bool:
    """非同期版: 指定されたIPアドレスが指定されたネットワークに属しているかどうかを判定する関数"""
    return await asyncio.to_thread(
        _sync.is_ip_in_allowed_networks, ipaddr, allow_networks
    )


async def domain_exists(domain: str) -> bool:
    """非同期版: 指定されたドメイン名が存在するかどうかを判定する関数"""
    return await asyncio.to_thread(_sync.domain_exists, domain)


async def get_country_ip_list(country: Country = Country.JP) -> list[str]:
    """非同期版: 特定の国のIPアドレスを取得（デフォルトは日本）"""
    return await asyncio.to_thread(_sync.get_country_ip_list, country)


async def is_country_ip(ipaddr: str, country: Country = Country.JP) -> bool:
    """非同期版: 指定されたアドレスが指定の国のIPアドレスか確認する関数（デフォルトは日本）"""
    return await asyncio.to_thread(_sync.is_country_ip, ipaddr, country)


async def get_japanip_list() -> list[str]:
    """非同期版: 日本のIPアドレスを取得する関数"""
    return await asyncio.to_thread(_sync.get_japanip_list)


async def is_japan_ip(ipaddr: str) -> bool:
    """非同期版: 指定されたアドレスが日本のIPアドレスか確認する関数"""
    return await asyncio.to_thread(_sync.is_japan_ip, ipaddr)


async def get_puny_code(domain: str) -> PunyDomainInfo:
    """非同期版: 日本語を含むドメインをpunycodeに変換する関数"""
    return await asyncio.to_thread(_sync.get_puny_code, domain)


async def get_adhost(domain: str | None = None) -> list[str]:
    """非同期版: 広告および危険なホストのリストを取得"""
    return await asyncio.to_thread(_sync.get_adhost, domain)


async def get_robots_txt_url(url: str) -> str:
    """非同期版: スクレイピング対象URLからrobots.txtファイルのURLを生成"""
    return await asyncio.to_thread(_sync.get_robots_txt_url, url)


async def is_scraping_allowed(url: str, user_agent: str = "*") -> bool:
    """非同期版: 指定されたURLに対してスクレイピングが許可されているかどうかを判定"""
    return await asyncio.to_thread(_sync.is_scraping_allowed, url, user_agent)

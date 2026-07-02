"""短縮URLサービスの非同期版クライアント。

同期版 :class:`~flaretool.shorturl.ShortUrlService` の各メソッドを
``asyncio.to_thread`` でワーカースレッドに委譲する薄いラッパーです。
イベントループをブロックせずに短縮URL APIを利用できます。

Warning:
    このクラスは更新される可能性があり、近い将来使用方法が変更される場合があります。
"""

import asyncio

from flaretool.shorturl.models import ShortUrlInfo
from flaretool.shorturl.ShortUrlService import ShortUrlService

__all__ = ["AsyncShortUrlService"]


class AsyncShortUrlService:
    """
    短縮URLサービスの非同期版クラス。

    同期版 :class:`ShortUrlService` をラップし、各メソッドを
    ``asyncio.to_thread`` 経由で実行します。
    非同期コンテキストマネージャー（``async with``）としても利用できます。

    Examples:
        >>> async with AsyncShortUrlService() as svc:
        ...     info = await svc.create("https://example.com")
        ...     print(info.short_url)
    """

    def __init__(self, _service: ShortUrlService | None = None) -> None:
        """AsyncShortUrlServiceを初期化する。

        Args:
            _service (ShortUrlService | None): ラップする同期版サービスの
                インスタンス。省略時は新規に生成します（テスト/DI用）。

        Raises:
            AuthenticationError: APIキーが設定されていない場合。
        """
        self._sync = _service if _service is not None else ShortUrlService()

    async def __aenter__(self) -> "AsyncShortUrlService":
        """非同期コンテキストマネージャーとして自身を返す。"""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        """終了処理（解放すべきリソースはないため何もしない）。"""
        return False

    async def get(self, id: int | None = None) -> list[ShortUrlInfo]:
        """非同期版: 短縮URLの情報一覧を取得する。

        Args:
            id (int | None): 短縮URLのID（デフォルト: None、全件取得）。

        Returns:
            list[ShortUrlInfo]: 短縮URLの情報リスト。

        Examples:
            >>> async with AsyncShortUrlService() as svc:
            ...     infos = await svc.get()
        """
        return await asyncio.to_thread(self._sync.get, id)

    async def create(
        self,
        url: str,
        code: str | None = None,
        description: str | None = None,
        is_eternal: bool | None = None,
        is_active: bool | None = None,
    ) -> ShortUrlInfo:
        """非同期版: 新しい短縮URLを作成する。

        Args:
            url (str): 短縮対象のURL。
            code (str | None): 短縮URLのカスタムコード（デフォルト: None）。
            description (str | None): 短縮URLの説明（デフォルト: None）。
            is_eternal (bool | None): 無期限とするか（デフォルト: None）。
            is_active (bool | None): 有効とするか（デフォルト: None）。

        Returns:
            ShortUrlInfo: 作成された短縮URLの情報。

        Examples:
            >>> async with AsyncShortUrlService() as svc:
            ...     info = await svc.create("https://example.com", code="abcd")
        """
        return await asyncio.to_thread(
            self._sync.create,
            url,
            code=code,
            description=description,
            is_eternal=is_eternal,
            is_active=is_active,
        )

    async def update(self, url_info: ShortUrlInfo) -> ShortUrlInfo:
        """非同期版: 短縮URLの情報を更新する。

        Args:
            url_info (ShortUrlInfo): 更新後の短縮URL情報。

        Returns:
            ShortUrlInfo: 更新された短縮URLの情報。

        Examples:
            >>> async with AsyncShortUrlService() as svc:
            ...     updated = await svc.update(url_info)
        """
        return await asyncio.to_thread(self._sync.update, url_info)

    async def delete(self, url_info: ShortUrlInfo) -> None:
        """非同期版: 短縮URLを削除する。

        Args:
            url_info (ShortUrlInfo): 削除対象の短縮URL情報。

        Examples:
            >>> async with AsyncShortUrlService() as svc:
            ...     await svc.delete(url_info)
        """
        return await asyncio.to_thread(self._sync.delete, url_info)

    async def get_qr_code_raw_data(self, url_info: ShortUrlInfo) -> bytes:
        """非同期版: QRコードの生データ（画像バイト列）を取得する。

        Args:
            url_info (ShortUrlInfo): 対象の短縮URL情報。

        Returns:
            bytes: 画像のバイトデータ。

        Examples:
            >>> async with AsyncShortUrlService() as svc:
            ...     raw = await svc.get_qr_code_raw_data(url_info)
        """
        return await asyncio.to_thread(self._sync.get_qr_code_raw_data, url_info)

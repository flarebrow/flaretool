"""DDNSサービスの非同期版クライアント。

同期版 :class:`~flaretool.ddns.DdnsService` の各メソッドを
``asyncio.to_thread`` でワーカースレッドに委譲する薄いラッパーです。
イベントループをブロックせずにDDNS APIを利用できます。

Warning:
    このクラスは更新される可能性があり、近い将来使用方法が変更される場合があります。
"""

import asyncio

from flaretool.ddns.DdnsService import DdnsService
from flaretool.ddns.models import DdnsInfo

__all__ = ["AsyncDdnsService"]


class AsyncDdnsService:
    """
    ダイナミックDNS（DDNS）サービスの非同期版クラス。

    同期版 :class:`DdnsService` をラップし、各メソッドを
    ``asyncio.to_thread`` 経由で実行します。
    非同期コンテキストマネージャー（``async with``）としても利用できます。

    Examples:
        >>> async with AsyncDdnsService() as svc:
        ...     info = await svc.update_ddns("example", "192.168.0.100")
        ...     print(info.domain)
    """

    def __init__(self, _service: DdnsService | None = None) -> None:
        """AsyncDdnsServiceを初期化する。

        Args:
            _service (DdnsService | None): ラップする同期版サービスの
                インスタンス。省略時は新規に生成します（テスト/DI用）。

        Raises:
            AuthenticationError: APIキーが設定されていない場合。
        """
        self._sync = _service if _service is not None else DdnsService()

    async def __aenter__(self) -> "AsyncDdnsService":
        """非同期コンテキストマネージャーとして自身を返す。"""
        return self

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        """終了処理（解放すべきリソースはないため何もしない）。"""
        return False

    async def update_ddns(self, host: str, ip: str | None = None) -> DdnsInfo:
        """非同期版: 指定したホストのダイナミックDNS（DDNS）を更新する。

        Args:
            host (str): DDNSを更新するホスト名。
            ip (str | None): 設定するIPアドレス。省略時は現在のIPが使用されます。

        Returns:
            DdnsInfo: 更新されたDDNSの情報。

        Examples:
            >>> async with AsyncDdnsService() as svc:
            ...     info = await svc.update_ddns("example", "192.168.0.100")
        """
        return await asyncio.to_thread(self._sync.update_ddns, host, ip)

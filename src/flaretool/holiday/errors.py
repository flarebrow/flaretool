"""祝日機能の例外定義"""

from flaretool.errors import FlareToolError


class JapaneseHolidaysError(FlareToolError):
    """祝日データの取得に失敗した場合に送出される例外"""

    def __init__(self, **kwargs):
        self.message = kwargs.get("message", "")
        super().__init__(self.message)

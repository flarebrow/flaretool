"""荷物追跡関連の関数群。"""

from flaretool.common import requests
from flaretool.constants import API_BASE_URL_OLD
from flaretool.decorators import network_required

__all__ = ["yamato", "japanpost"]

#: ヤマト運輸APIが一度に受け付ける追跡番号の最大件数
_YAMATO_MAX_CODES = 10


def _insert_str(text: str, insert: str, num: int) -> str:
    """text を num 文字ごとに insert で区切った文字列を返す内部ヘルパー。"""
    return insert.join(text[i : i + num] for i in range(0, len(text), num))


def _format_code(code: str) -> str:
    """追跡番号をAPIが期待する ``XXXX-XXXX-XXXX-X`` 形式に整形する。"""
    if len(code) != 14:
        code = _insert_str(code.strip(), "-", 4)
    return code


@network_required
def yamato(codes: list[str]) -> list[dict]:
    """
    ヤマト運輸の荷物追跡をする関数

    Args:
        codes (list[str]): 追跡番号のリスト(Max10件)

    Returns:
        list[dict]: 取得結果

    Raises:
        ValueError: 追跡番号が10件を超えている場合
    """
    codes = [str(code) for code in codes]
    if len(codes) > _YAMATO_MAX_CODES:
        raise ValueError(
            f"yamato() accepts at most {_YAMATO_MAX_CODES} tracking codes "
            f"(got {len(codes)})."
        )
    params = {f"n{i}": _format_code(code) for i, code in enumerate(codes, 1)}
    return requests.get(
        f"{API_BASE_URL_OLD}/yamato",
        params=params,
    ).json()["result"]


@network_required
def japanpost(code: str) -> dict:
    """
    日本郵便の荷物追跡をする関数

    Args:
        code (str): 追跡番号

    Returns:
        dict: 取得結果
    """
    return requests.get(
        f"{API_BASE_URL_OLD}/japanpost",
        params={"n": _format_code(code)},
    ).json()

#!/bin/python
# -*- coding: utf-8 -*-
from flaretool.decorators import network_required
from flaretool.constants import BASE_API_URL


@network_required
def yamato(codes: list[str]) -> list[dict]:
    """
    ヤマト運輸の荷物追跡をする関数 

    Args:
        codes (list[str]): 追跡番号のリスト(Max10件)

    Returns:
        list[dict]: 取得結果
    """
    from flaretool.common import requests

    def __insert_str(text: str, insert: str, num: int):
        return insert.join(text[i:i+num] for i in range(0, len(text), num))
    codes = list(map(str, codes))
    post_data = {}
    number_list = []
    for i, code in enumerate(codes, 1):
        if (len(code) != 14):
            code = __insert_str(code.strip(), "-", 4)
        number_list.append(code)
        post_data[f"n{str(i)}"] = code
    return requests.get(
        f"{BASE_API_URL}/yamato",
        params=post_data,
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
    from flaretool.common import requests

    def __insert_str(text: str, insert: str, num: int):
        return insert.join(text[i:i+num] for i in range(0, len(text), num))

    post_data = {}
    number_list = []
    if (len(code) != 14):
        code = __insert_str(code.strip(), "-", 4)
    number_list.append(code)
    post_data["n"] = code
    return requests.get(
        f"{BASE_API_URL}/japanpost",
        params=post_data,
    ).json()


__all__ = ["yamato", "japanpost"]

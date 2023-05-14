#!/bin/python
# -*- coding: utf-8 -*-


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
        "https://api.flarebrow.com/v2/yamato",
        params=post_data,
    ).json()["result"]


__all__ = []

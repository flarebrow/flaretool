"""Amazon商品情報の取得関数。"""

import warnings

from flaretool.common import requests
from flaretool.constants import API_BASE_URL_OLD
from flaretool.decorators import network_required
from flaretool.funcs.models import AmazonInfo

# AmazonInfo は従来から ``from flaretool.funcs.amazon import *`` で
# 参照できたため、後方互換のため再エクスポートする
__all__ = ["amazon_info", "AmazonInfo"]


@network_required
def amazon_info(url: str) -> AmazonInfo:
    """
    Fetches Amazon product information using the provided URL.
    Args:
        url (str): The Amazon product URL.
    Returns:
        AmazonInfo: An instance of AmazonInfo containing the product information.
    Warning:
        This feature is unstable. It is considered experimental and subject to potential changes in future versions.
    """
    warnings.warn(
        "This feature is unstable. It is considered experimental and subject "
        "to potential changes in future versions.",
        Warning,
        stacklevel=2,
    )
    result = requests.post(f"{API_BASE_URL_OLD}/amazon", data={"url": url})
    return AmazonInfo(**result.json())

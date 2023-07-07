#!/bin/python
# -*- coding: utf-8 -*-
import warnings
from flaretool.decorators import network_required
from .models import AmazonInfo


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
    message = "This feature is unstable. It is considered experimental and subject to potential changes in future versions."
    warnings.warn(message, DeprecationWarning)
    from flaretool.common import requests
    result = requests.post(
        "https://api.flarebrow.com/v2/amazon", data={"url": url})
    result_json = result.json()
    return AmazonInfo(**result_json)

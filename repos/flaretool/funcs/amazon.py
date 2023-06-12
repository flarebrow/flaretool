from flaretool.decorators import network_required
from .models import AmazonInfo


@network_required
def amazon_info(url: str):
    from flaretool.common import requests
    result = requests.get(
        "https://api.flarebrow.com/v2/amazon", params={"url": url})
    result_json = result.json()
    return AmazonInfo(**result_json)

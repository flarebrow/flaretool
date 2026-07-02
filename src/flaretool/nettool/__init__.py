"""Network tools for flaretool."""

from flaretool.nettool.common import (
    IpInfo as IpInfo,
)
from flaretool.nettool.common import (
    PunyDomainInfo as PunyDomainInfo,
)
from flaretool.nettool.common import (
    domain_exists,
    get_adhost,
    get_country_ip_list,
    get_global_ipaddr_info,
    get_japanip_list,
    get_puny_code,
    get_robots_txt_url,
    is_country_ip,
    is_ip_in_allowed_networks,
    is_japan_ip,
    is_scraping_allowed,
    lookup_domain,
    lookup_ip,
)

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
    # モデルクラスは flaretool.nettool.models から明示的にインポートする
    # （属性アクセス nettool.IpInfo は引き続き可能）
    # "IpInfo",
    # "PunyDomainInfo",
]

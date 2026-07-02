"""Network utility functions."""

import ipaddress
import socket
from urllib import robotparser
from urllib.parse import urlparse, urlunparse

from flaretool.common import requests
from flaretool.constants import (
    ADHOST_DATA_URL,
    API_BASE_URL_OLD,
    COUNTRY_IPV4_DATA_URL,
    Country,
)
from flaretool.logger import get_logger
from flaretool.nettool.models import IpInfo, PunyDomainInfo

logger = get_logger()


def get_global_ipaddr_info(addr: str | None = None) -> IpInfo:
    """
    指定されたグローバルIPアドレスの情報を取得する関数
    (指定がない場合は実行端末のグローバルIPを取得)

    Args:
        addr (str): IPアドレス または ホスト名（デフォルトはNone）

    Returns:
        IpInfo: IPアドレスの情報(取得できない項目はNoneをセット)

    """
    path = "" if addr is None else f"/{addr}"
    result = requests.get(f"{API_BASE_URL_OLD}/ip{path}").json()
    return IpInfo(**result)


def lookup_ip(domain: str) -> str | None:
    """
    指定されたドメイン名からIPアドレスを取得する関数

    Args:
        domain (str): ドメイン名

    Returns:
        str | None: IPアドレス（取得できない場合はNone）

    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        logger.error(f"Error during forward DNS lookup: {e}")
        return None


def lookup_domain(ip: str) -> str | None:
    """
    指定されたIPアドレスからドメイン名を取得する関数

    Args:
        ip (str): IPアドレス

    Returns:
        str | None: ドメイン名（取得できない場合はNone）

    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror as e:
        logger.error(f"Error during reverse DNS lookup: {e}")
        return None


def is_ip_in_allowed_networks(ipaddr: str, allow_networks: list[str]) -> bool:
    """
    指定されたIPアドレスが指定されたネットワークに属しているかどうかを判定する関数

    Args:
        ipaddr (str): IPアドレス
        allow_networks (list[str]): 許可されたネットワークのリスト

    Returns:
        bool: 指定されたIPアドレスが指定されたネットワークに属している場合はTrue、それ以外の場合はFalse

    """
    ip_networks = [ipaddress.ip_network(network) for network in allow_networks]
    remote_addr = ipaddress.ip_address(ipaddr)
    return any(remote_addr in ip_network for ip_network in ip_networks)


def domain_exists(domain: str) -> bool:
    """
    指定されたドメイン名が存在するかどうかを判定する関数

    Args:
        domain (str): ドメイン名

    Returns:
        bool: 指定されたドメイン名が存在する場合はTrue、それ以外の場合はFalse

    """
    # whois はインポートが重いため、モジュールインポート時ではなく
    # 実際に使用するこの関数内で読み込む（オフライン系コマンドの起動を軽くする）
    import whois

    try:
        w = whois.whois(domain)
        return bool(w.status)
    except Exception:
        # python-whois は壊れやすく、バージョンによって送出される例外の
        # 種類が異なる（PywhoisError / socket系 / AttributeError など）ため、
        # 意図的にすべての例外をキャッチしてFalseを返す
        return False


def get_country_ip_list(country: Country = Country.JP) -> list[str]:
    """
    特定の国のIPアドレスを取得（デフォルトは日本）

    Args:
        country (Country, optional): 国コード. Defaults to Country.JP.

    Returns:
        list[str]: IPアドレスのリスト
    """
    return requests.get(COUNTRY_IPV4_DATA_URL.format(cc=country.name)).text.splitlines()


def is_country_ip(ipaddr: str, country: Country = Country.JP) -> bool:
    """
    指定されたアドレスが指定の国のIPアドレスか確認する関数（デフォルトは日本）

    Args:
        ipaddr (str): IPアドレス
        country (Country, optional): 国コード. Defaults to Country.JP.

    Returns:
        bool: 指定されたIPアドレスが指定した国のIPの場合はTrue、それ以外の場合はFalse
    """
    return is_ip_in_allowed_networks(ipaddr, get_country_ip_list(country))


def get_japanip_list() -> list[str]:
    """
    日本のIPアドレスを取得する関数

    Returns:
        list[str]: 日本のIPアドレスのリスト
    """
    return get_country_ip_list()


def is_japan_ip(ipaddr: str) -> bool:
    """
    指定されたアドレスが日本のIPアドレスか確認する関数

    Args:
        ipaddr (str): IPアドレス

    Returns:
        bool: 指定されたIPアドレスが日本のIPの場合はTrue、それ以外の場合はFalse
    """
    return is_ip_in_allowed_networks(ipaddr, get_japanip_list())


def get_puny_code(domain: str) -> PunyDomainInfo:
    """
    日本語を含むドメインをpunycodeに変換する関数

    Args:
        domain (str): ドメイン名

    Returns:
        PunyDomainInfo: 取得結果
    """
    result = requests.get(f"{API_BASE_URL_OLD}/puny/{domain}").json()
    return PunyDomainInfo(**result)


def get_adhost(domain: str | None = None) -> list[str]:
    """
    広告および危険なホストのリストを取得

    Args:
        domain (str, optional): 検索ドメイン（デフォルトはNone）

    Returns:
        list[str]: ホストリスト
    """
    hosts = []
    for line in requests.get(ADHOST_DATA_URL).text.splitlines():
        # "#" 以降はコメントとして除去（行全体がコメントの場合は行ごと除外）
        host = line.split("#", 1)[0].strip()
        if host:
            hosts.append(host)
    return hosts if domain is None else [host for host in hosts if domain in host]


def get_robots_txt_url(url: str) -> str:
    """
    スクレイピング対象URLからrobots.txtファイルのURLを生成

    Args:
        url (str): スクレイピング対象のURL

    Returns:
        str: robots.txtファイルのURL
    """
    parsed_url = urlparse(url)
    return urlunparse((parsed_url.scheme, parsed_url.netloc, "/robots.txt", "", "", ""))


def is_scraping_allowed(url: str, user_agent: str = "*") -> bool:
    """
    指定されたURLに対してスクレイピングが許可されているかどうかを判定

    Args:
        url (str): スクレイピング対象のURL
        user_agent (str, optional): 使用するユーザーエージェント デフォルトは"*"

    Returns:
        bool: スクレイピングが許可されている場合はTrue、禁止されている場合はFalse
    """
    rp = robotparser.RobotFileParser()
    # robots.txtファイルのURLを設定
    rp.set_url(get_robots_txt_url(url))
    rp.read()
    # 指定されたURLに対するスクレイピングが許可されているかどうかを判断
    return rp.can_fetch(user_agent, url)

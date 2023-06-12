#!/bin/python
# -*- coding: utf-8 -*-
import os
import tempfile
import socket
import whois
import ipaddress
from .models import IpInfo, PunyDomainInfo
from flaretool.common import requests
from urllib import robotparser
from urllib.parse import urlparse, urlunparse


def get_global_ipaddr_info(addr: str = None) -> IpInfo:
    """
    指定されたグローバルIPアドレスの情報を取得する関数
    (指定がない場合は実行端末のグローバルIPを取得)

    Args:
        addr (str): IPアドレス または ホスト名（デフォルトはNone）

    Returns:
        IpInfo: IPアドレスの情報(取得できない項目はNoneをセット)

    """
    addr = "" if addr is None else f"/{addr}"
    result = requests.get(
        f"https://api.flarebrow.com/v2/ip{addr}".format()).json()
    return IpInfo(**result)


def lookup_ip(domain: str) -> str:
    """
    指定されたドメイン名からIPアドレスを取得する関数

    Args:
        domain (str): ドメイン名

    Returns:
        str: IPアドレス

    """
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"Error during forward DNS lookup: {e}")
        return None


def lookup_domain(ip: str) -> str:
    """
    指定されたIPアドレスからドメイン名を取得する関数

    Args:
        ip (str): IPアドレス

    Returns:
        str: ドメイン名

    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror as e:
        print(f"Error during reverse DNS lookup: {e}")
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
    try:
        w = whois.whois(domain)
        return True if w.status else False
    except whois.parser.PywhoisError:
        return False


def get_japanip_list() -> list[str]:
    """
    日本のIPアドレスを取得する関数

    Returns:
        list[str]: 日本のIPアドレスのリスト
    """
    return requests.get(
        "https://raw.githubusercontent.com/flarebrow/public/master/IPAddress/japan_ipv4.txt"
    ).text.splitlines()


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
    result = requests.get(f"https://api.flarebrow.com/v2/puny/{domain}").json()
    return PunyDomainInfo(**result)


def get_adhost(domain: str = None) -> list[str]:
    """
    広告および危険なホストのリストを取得

    Args:
        domain (str, optional): 検索ドメイン（デフォルトはNone）

    Returns:
        list[str]: ホストリスト
    """
    url = "https://raw.githubusercontent.com/flarebrow/public/master/Adhost/hostlist.txt"

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, os.path.basename(url))

        with open(file_path, "wb") as file:
            response = requests.get(url)
            file.write(response.content)

        with open(file_path, "r") as file:
            file_content_list = [
                host for host in file.read().splitlines() if "#" not in host]
            return file_content_list if domain is None else [host for host in file_content_list if domain in host]


def get_robots_txt_url(url: str) -> str:
    """
    スクレイピング対象URLからrobots.txtファイルのURLを生成

    Args:
        url (str): スクレイピング対象のURL

    Returns:
        str: robots.txtファイルのURL
    """
    parsed_url = urlparse(url)
    robots_txt_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, '/robots.txt', '', '', ''))
    return robots_txt_url


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


__all__ = []

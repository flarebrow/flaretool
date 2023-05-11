#!/bin/python
# -*- coding: utf-8 -*-
import inspect
import argparse
import flaretool
from flaretool import nettool

current_ver = flaretool.__version__

description = """
{} ver{}
""".format(flaretool.__name__, current_ver)


def main():

    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_nettool = subparsers.add_parser('nettool')
    parser_nettool.add_argument(
        "mode", choices=["info"] + [func for func in dir(
            nettool) if inspect.isfunction(getattr(nettool, func))]
    )
    parser_nettool.add_argument('args', nargs='*', default=[])

    args = parser.parse_args()

    if args.command == 'nettool':
        if args.mode == "info":
            network_info = nettool.get_global_ipaddr_info()
            print("=== Your IP Infomation ===")
            print("ip:", network_info.ipaddr)
            print("hostname:", network_info.hostname)
            print("country:", network_info.country)
        else:
            try:
                print(getattr(nettool, args.mode)(*args.args))
            except TypeError as e:
                print(e)
                return 9
    return 0

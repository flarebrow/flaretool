#!/bin/python
# -*- coding: utf-8 -*-
import sys
import inspect
import argparse
import flaretool
from flaretool import nettool
from flaretool.basemodels import BaseDataModel

current_ver = flaretool.__version__

description = """
{} ver{}
""".format(flaretool.__name__, current_ver)


def cli():

    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest='func', required=True)

    parser_nettool = subparsers.add_parser('nettool')
    nettool_func_list = [func for func in dir(
        nettool) if inspect.isfunction(getattr(nettool, func))]
    nettool_func_doc = ""
    for func in nettool_func_list:
        method = getattr(nettool, func)
        doc = method.__doc__.splitlines()[1].strip(
        ) if method.__doc__ else "unknown"
        nettool_func_doc += f"[{method.__name__}]:{doc} \t"
    parser_nettool.add_argument(
        "mode",
        choices=["info"] + nettool_func_list,
        help=nettool_func_doc,
    )
    parser_nettool.add_argument('args', nargs='*', default=[], help="引数")

    args = parser.parse_args()

    if args.func == 'nettool':
        if args.mode == "info":
            network_info = nettool.get_global_ipaddr_info()
            print("=== Your IP Infomation ===")
            print("ip:", network_info.ipaddr)
            print("hostname:", network_info.hostname)
            print("country:", network_info.country)
        else:
            try:
                result = getattr(nettool, args.mode)(*args.args)
                print(result if not isinstance(
                    result, BaseDataModel) else result.__trace__())
            except TypeError as e:
                print(e)
                return 1
    return 0


def main():
    sys.exit(cli())

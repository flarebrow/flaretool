#!/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import json
import platform
import requests as req
from requests.models import Response
from flaretool.logger import get_logger
import flaretool

logger = get_logger()


class requests():

    @staticmethod
    def request(method: str, url: str, **kwargs) -> Response:
        from urllib.parse import urlparse
        headers = kwargs.pop("headers", {})
        ua = {
            "Mozilla": "5.0",
            "publisher": flaretool.__name__,
            "flaretool": flaretool.VERSION,
            "lang_version": platform.python_version(),
            "os": platform.system(),
            "platform": platform.platform(),
        }
        user_agent = " ".join([f"{key}/{value}" for key, value in ua.items()])
        headers["User-Agent"] = user_agent
        headers["X-UA"] = user_agent
        if "flarebrow.com" in urlparse(url).netloc:
            headers["X-FLAREBROW-AUTH"] = flaretool.api_key
        with req.Session() as session:
            response = session.request(
                method=method, url=url, headers=headers, **kwargs)
            logger.debug(
                {
                    "status_code": response.status_code,
                    "method": method,
                    "url": url,
                    "param": kwargs.get("param", {}),
                    "data": kwargs.get("data", {}),
                }
            )
            return response

    @staticmethod
    def get(url, **kwargs) -> Response:
        return requests.request("GET", url, **kwargs)

    @staticmethod
    def post(url, **kwargs) -> Response:
        return requests.request("POST", url, **kwargs)

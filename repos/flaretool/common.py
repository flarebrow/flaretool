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
from flaretool.errors import FlareToolNetworkError

logger = get_logger()


class requests():

    @staticmethod
    def request(method: str, url: str, auth_enabled: bool = False, **kwargs) -> Response:
        """
        Send an HTTP request with the specified method, URL, and optional parameters.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            url (str): The URL to send the request to.
            auth_enabled (bool, optional): Whether to force authentication for the request. Defaults to False.
            **kwargs: Additional keyword arguments to be passed to the underlying request method.

        Returns:
            Response: The response object representing the server's response to the request.

        Raises:
            FlareToolNetworkError: If the request is made to a Flare service and the response status code is 403.

        """
        headers = kwargs.pop("headers", {})
        ua = {
            "Mozilla": "5.0",
            "publisher": flaretool.__name__,
            "flaretool": flaretool.__version__,
            "lang_version": platform.python_version(),
            "os": platform.system(),
            "platform": platform.platform(),
        }
        user_agent = " ".join([f"{key}/{value}" for key, value in ua.items()])
        headers["User-Agent"] = user_agent
        headers["X-UA"] = user_agent
        if auth_enabled:
            params = kwargs.get("params", {})
            params["apikey"] = flaretool.api_key
            kwargs.update({"params": params})
            headers["Authorization"] = f"Bearer {flaretool.api_key}"
            headers["X-FLAREBROW-AUTH"] = flaretool.api_key
        with req.Session() as session:
            response = session.request(
                method=method, url=url, headers=headers, **kwargs)
            logger.debug(
                {
                    "status_code": response.status_code,
                    "method": method,
                    "url": url,
                    "params": kwargs.get("params", {}),
                    "data": kwargs.get("data", {}),
                }
            )
            if (auth_enabled or "flarebrow.com" in response.url) and response.status_code == 403:
                raise FlareToolNetworkError(
                    message="Only access from Japan is accepted"
                )
            return response

    @staticmethod
    def get(url, **kwargs) -> Response:
        return requests.request("GET", url, **kwargs)

    @staticmethod
    def post(url, **kwargs) -> Response:
        return requests.request("POST", url, **kwargs)

    @staticmethod
    def put(url, **kwargs) -> Response:
        return requests.request("PUT", url, **kwargs)

    @staticmethod
    def delete(url, **kwargs) -> Response:
        return requests.request("DELETE", url, **kwargs)

    @staticmethod
    def head(url, **kwargs) -> Response:
        kwargs.setdefault("allow_redirects", False)
        return requests.request("HEAD", url, **kwargs)

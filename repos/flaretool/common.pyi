from typing import Optional, Mapping, Union
from requests.models import Response
from requests.sessions import RequestsCookieJar, _Auth, _Cert, _Data, _Files, _HooksInput, _Params, _TextMapping, _Timeout, _Verify

_HeadersMapping = Mapping[str, Union[str, bytes]]


class requests:
    @staticmethod
    def request(
        method: str,
        url: Union[str, bytes],
        *,
        params: Optional[_Params] = None,
        data: Optional[_Data] = None,
        headers: Optional[_HeadersMapping] = None,
        cookies: Optional[Union[RequestsCookieJar, _TextMapping]] = None,
        files: Optional[_Files] = None,
        auth: Optional[_Auth] = None,
        timeout: Optional[_Timeout] = None,
        allow_redirects: bool = True,
        proxies: Optional[_TextMapping] = None,
        hooks: Optional[_HooksInput] = None,
        stream: Optional[bool] = None,
        verify: Optional[_Verify] = None,
        cert: Optional[_Cert] = None,
        json: Optional[Union[dict, list]] = None,
        auth_enabled: Optional[bool] = False,
    ) -> Response: ...

    @staticmethod
    def get(
        url: Union[str, bytes],
        params: Optional[_Params] = None,
        *,
        data: Optional[_Data] = None,
        headers: Optional[_HeadersMapping] = None,
        cookies: Optional[Union[RequestsCookieJar, _TextMapping]] = None,
        files: Optional[_Files] = None,
        auth: Optional[_Auth] = None,
        timeout: Optional[_Timeout] = None,
        allow_redirects: bool = True,
        proxies: Optional[_TextMapping] = None,
        hooks: Optional[_HooksInput] = None,
        stream: Optional[bool] = None,
        verify: Optional[_Verify] = None,
        cert: Optional[_Cert] = None,
        json: Optional[Union[dict, list]] = None,
        auth_enabled: Optional[bool] = False,
    ) -> Response: ...

    @staticmethod
    def post(
        url: Union[str, bytes],
        *,
        params: Optional[_Params] = None,
        data: Optional[_Data] = None,
        headers: Optional[_HeadersMapping] = None,
        cookies: Optional[Union[RequestsCookieJar, _TextMapping]] = None,
        files: Optional[_Files] = None,
        auth: Optional[_Auth] = None,
        timeout: Optional[_Timeout] = None,
        allow_redirects: bool = True,
        proxies: Optional[_TextMapping] = None,
        hooks: Optional[_HooksInput] = None,
        stream: Optional[bool] = None,
        verify: Optional[_Verify] = None,
        cert: Optional[_Cert] = None,
        json: Optional[Union[dict, list]] = None,
        auth_enabled: Optional[bool] = False,
    ) -> Response: ...

    @staticmethod
    def put(
        url: Union[str, bytes],
        *,
        params: Optional[_Params] = None,
        data: Optional[_Data] = None,
        headers: Optional[_HeadersMapping] = None,
        cookies: Optional[Union[RequestsCookieJar, _TextMapping]] = None,
        files: Optional[_Files] = None,
        auth: Optional[_Auth] = None,
        timeout: Optional[_Timeout] = None,
        allow_redirects: bool = True,
        proxies: Optional[_TextMapping] = None,
        hooks: Optional[_HooksInput] = None,
        stream: Optional[bool] = None,
        verify: Optional[_Verify] = None,
        cert: Optional[_Cert] = None,
        json: Optional[Union[dict, list]] = None,
        auth_enabled: Optional[bool] = False,
    ) -> Response: ...

    @staticmethod
    def delete(
        url: Union[str, bytes],
        *,
        params: Optional[_Params] = None,
        data: Optional[_Data] = None,
        headers: Optional[_HeadersMapping] = None,
        cookies: Optional[Union[RequestsCookieJar, _TextMapping]] = None,
        files: Optional[_Files] = None,
        auth: Optional[_Auth] = None,
        timeout: Optional[_Timeout] = None,
        allow_redirects: bool = True,
        proxies: Optional[_TextMapping] = None,
        hooks: Optional[_HooksInput] = None,
        stream: Optional[bool] = None,
        verify: Optional[_Verify] = None,
        cert: Optional[_Cert] = None,
        json: Optional[Union[dict, list]] = None,
        auth_enabled: Optional[bool] = False,
    ) -> Response: ...

    @staticmethod
    def head(
        url: Union[str, bytes],
        *,
        params: Optional[_Params] = None,
        data: Optional[_Data] = None,
        headers: Optional[_HeadersMapping] = None,
        cookies: Optional[Union[RequestsCookieJar, _TextMapping]] = None,
        files: Optional[_Files] = None,
        auth: Optional[_Auth] = None,
        timeout: Optional[_Timeout] = None,
        allow_redirects: bool = True,
        proxies: Optional[_TextMapping] = None,
        hooks: Optional[_HooksInput] = None,
        stream: Optional[bool] = None,
        verify: Optional[_Verify] = None,
        cert: Optional[_Cert] = None,
        json: Optional[Union[dict, list]] = None,
        auth_enabled: Optional[bool] = False,
    ) -> Response: ...

from _typeshed import Incomplete
from collections.abc import Mapping
from typing_extensions import TypeAlias
from requests.models import Response
from requests.sessions import RequestsCookieJar, _Auth, _Cert, _Data, _Files, _HooksInput, _Params, _TextMapping, _Timeout, _Verify

_HeadersMapping: TypeAlias = Mapping[str, str | bytes]


class requests:
    def request(
        method: str,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> Response: ...

    def get(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> Response: ...

    def post(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> Response: ...

    def put(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> Response: ...

    def delete(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> Response: ...

    def head(
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> Response: ...

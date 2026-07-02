"""
flaretool python module
[Terms of service](https://main.flarebrow.com/terms)
"""

import importlib
import logging
import warnings
from types import ModuleType

from flaretool import logger  # noqa: F401  (public re-export, kept lightweight)
from flaretool.settings import get_settings
from flaretool.VERSION import VERSION

logging.getLogger(__name__).addHandler(logging.NullHandler())

# NOTE: ``settings`` and ``api_key`` are documented *mutable* module globals.
# ``flaretool.api_key`` may be reassigned at runtime (e.g. ``flaretool.api_key
# = "..."`` in user code or by the CLI) and is re-read by flaretool.common on
# every authenticated request, so reassignment takes effect immediately.
settings = get_settings()
api_key: str | None = settings.api_key

# Submodules imported lazily via PEP 562 to avoid heavy import-time
# dependencies (e.g. ``nettool`` pulls in whois).
_LAZY_SUBMODULES = frozenset({"nettool"})


def __getattr__(name: str) -> ModuleType:
    if name in _LAZY_SUBMODULES:
        return importlib.import_module(f"{__name__}.{name}")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def get_lib_version() -> str:
    """Return the installed flaretool version."""
    return VERSION


def get_latest_version() -> str:
    """Return the latest flaretool version published on PyPI.

    Falls back to the installed version if PyPI cannot be reached.
    """
    try:
        # NOTE: intentionally uses the plain ``requests`` library instead of
        # ``flaretool.common.requests`` — the shared session mounts a retry
        # policy that can stall CLI startup for many seconds when the network
        # is unreachable. A short timeout and no retries keep the version
        # check cheap; any failure falls back to the installed version.
        import requests as _requests

        return _requests.get("https://pypi.org/pypi/flaretool/json", timeout=3).json()[
            "info"
        ]["version"]
    except Exception:
        return VERSION


def check_version() -> None:
    """Warn if a newer flaretool release is available on PyPI.

    This check is opt-in: it is intentionally *not* executed at import time
    (importing the package must not perform network I/O).
    """
    from packaging.version import parse

    current_ver = VERSION
    latest_ver = get_latest_version()
    if parse(current_ver) < parse(latest_ver):
        warnings.warn(
            f"flaretool {latest_ver} has been released (you are using "
            f"{current_ver}). Please update to the latest version.",
            stacklevel=2,
        )


__version__ = get_lib_version()
__all__ = [
    "api_key",
    "settings",
    "logger",
    "get_lib_version",
    "get_latest_version",
    "check_version",
]

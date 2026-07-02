"""Deprecated alias for :mod:`flaretool.utils`.

このモジュールは後方互換のために残されています。
新しいコードでは ``flaretool.utils`` を使用してください。

.. deprecated::
    ``flaretool.utills`` は非推奨です。``flaretool.utils`` に置き換えられました。
"""

import warnings as _warnings

_warnings.warn(
    "'flaretool.utills' is deprecated; use 'flaretool.utils' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# utils.py には __all__ が無いため、アンダースコアで始まらない全ての
# モジュールレベル名 (関数/クラス/定数/enum、さらに import された
# flaretool 等のモジュールオブジェクトも含む) が再エクスポートされる。
from flaretool.utils import *  # noqa: F401,F403,E402

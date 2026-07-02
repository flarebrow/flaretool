"""Tests for the deprecated flaretool.utills shim module."""

import importlib
import sys
import unittest
import warnings


class UtillsShimTestCase(unittest.TestCase):
    def test_import_emits_deprecation_warning(self):
        # Remove cached module so the module-level warning fires again.
        sys.modules.pop("flaretool.utills", None)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.import_module("flaretool.utills")
        deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        self.assertTrue(deprecations, "importing flaretool.utills should warn")
        self.assertIn("flaretool.utils", str(deprecations[0].message))

    def test_shim_reexports_utils_objects(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            import flaretool.utills
            import flaretool.utils

        self.assertIs(flaretool.utills.convert_value, flaretool.utils.convert_value)
        self.assertIs(flaretool.utills.hash_value, flaretool.utils.hash_value)
        self.assertIs(flaretool.utills.base64_convert, flaretool.utils.base64_convert)
        self.assertIs(
            flaretool.utills.DictToFieldConverter,
            flaretool.utils.DictToFieldConverter,
        )

    def test_enums_and_constants_importable_from_shim(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from flaretool.utills import (  # noqa: F401
                ASCII_ZENKAKU_CHARS,
                Base64Mode,
                ConversionMode,
                HashMode,
                flaretool,
            )

        self.assertEqual(flaretool.__name__, "flaretool")
        self.assertEqual(ConversionMode.HALF_WIDTH.value, 1)


if __name__ == "__main__":
    unittest.main()

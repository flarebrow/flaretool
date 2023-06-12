import unittest
from flaretool.errors import *


class ErrorTest(unittest.TestCase):

    def test_flaretool_error(self):
        error = FlareToolError("message")
        self.assertEqual(str(error), "message")
        self.assertEqual(repr(error), "<FlareToolError(message='message')>")

    def test_flaretool_network_error(self):
        error = FlareToolNetworkError("message")
        self.assertEqual(str(error), "message")
        # self.assertEqual(repr(error), "<FlareToolError(message='message')>")

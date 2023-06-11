import unittest
from unittest.mock import MagicMock, patch

from flaretool.funcs.amazon import amazon_info, AmazonInfo
from flaretool.funcs.tracking import *


class FuncsTest(unittest.TestCase):

    def setUp(self):
        self.mock_create_connection = MagicMock()
        self.mock_create_connection.return_value = None
        # self.mock_create_connection.side_effect = OSError
        self.patcher = patch("socket.create_connection",
                             self.mock_create_connection)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch("flaretool.common.requests.get")
    def test_amazon_info(self, mock_requests):
        url = "https://www.amazon.com/example-product"
        response_data = {
            "url": url,
            "title": "Example Product",
            "price": 100,
            "stock": "In Stock",
            "distributor": "Amazon",
            "sender": "Amazon",
            "evaluation": "4.5/5",
        }
        mock_requests.return_value.json.return_value = response_data

        info = amazon_info(url)

        self.assertIsInstance(info, AmazonInfo)
        self.assertEqual(info.url, url)
        self.assertEqual(info.title, "Example Product")
        self.assertEqual(info.price, 100)
        self.assertEqual(info.stock, "In Stock")
        self.assertEqual(info.distributor, "Amazon")
        self.assertEqual(info.sender, "Amazon")
        self.assertEqual(info.evaluation, "4.5/5")
        mock_requests.assert_called_once_with(
            "https://api.flarebrow.com/v2/amazon", params={"url": url}
        )

    @patch("flaretool.common.requests.get")
    def test_yamato(self, mock_get):
        codes = ["1234567890123", "9876543210987"]
        response_data = {"result": [
            {"status": "Delivered"}, {"status": "In Transit"}]}
        mock_get.return_value.json.return_value = response_data

        result = yamato(codes)

        self.assertEqual(result, response_data["result"])
        mock_get.assert_called_once_with(
            "https://api.flarebrow.com/v2/yamato",
            params={"n1": "1234-5678-9012-3", "n2": "9876-5432-1098-7"},
        )

    @patch("flaretool.common.requests.get")
    def test_japanpost(self, mock_get):
        code = "1234567890123"
        response_data = {"status": "In Transit"}
        mock_get.return_value.json.return_value = response_data

        result = japanpost(code)

        self.assertEqual(result, response_data)
        mock_get.assert_called_once_with(
            "https://api.flarebrow.com/v2/japanpost",
            params={"n": "1234-5678-9012-3"},
        )

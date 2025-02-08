import logging
import logging.handlers
import unittest

import flaretool
from flaretool.logger import *


class TestLogging(unittest.TestCase):
    def test_setup_logger_console(self):
        logger = setup_logger(loglevel=logging.DEBUG, console=True)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

    def test_setup_logger_file(self):
        logger = setup_logger(
            loglevel=logging.DEBUG, console=False, file=True, file_name="test.log"
        )
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.FileHandler)
        self.assertTrue(logger.handlers[0].baseFilename.endswith("test.log"))

    def test_setup_logger_rotating_file(self):
        logger = setup_logger(
            loglevel=logging.DEBUG, file=True, rotating=True, console=False
        )
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.handlers.RotatingFileHandler)

    def test_setup_logger_multiple_handlers(self):
        logger = setup_logger(loglevel=logging.DEBUG, file=True, file_name="test.log")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(len(logger.handlers), 2)
        self.assertIsInstance(logger.handlers[0], logging.FileHandler)
        self.assertTrue(logger.handlers[0].baseFilename.endswith("test.log"))
        self.assertIsInstance(logger.handlers[1], logging.StreamHandler)

    def test_setup_logger_extra(self):
        logger = setup_logger(loglevel=logging.DEBUG, extra=True)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)
        self.assertTrue("lineno" in logger.handlers[0].formatter._fmt)

    def test_get_logger(self):
        logger = get_logger()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, flaretool.__name__)

    def test_setup_logger_default_values(self):
        logger = setup_logger(console=False)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.getEffectiveLevel(), logging.INFO)
        self.assertEqual(len(logger.handlers), 0)

    def test_setup_logger_custom_values(self):
        logger = setup_logger(
            loglevel=logging.DEBUG,
            console=True,
            file=True,
            file_name="test.log",
            rotating=True,
        )
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.getEffectiveLevel(), logging.DEBUG)
        self.assertEqual(len(logger.handlers), 2)
        self.assertIsInstance(logger.handlers[0], logging.handlers.RotatingFileHandler)
        self.assertTrue(logger.handlers[0].baseFilename.endswith("test.log"))
        self.assertIsInstance(logger.handlers[1], logging.StreamHandler)

    def test_setup_logger_invalid_file_name(self):
        with self.assertRaises(FileNotFoundError):
            setup_logger(
                loglevel=logging.DEBUG,
                file=True,
                file_name="/invalid/path/test.log",
                console=False,
            )

    def test_setup_logger_invalid_max_bytes(self):
        with self.assertRaises(ValueError):
            setup_logger(
                loglevel=logging.DEBUG,
                file=True,
                rotating=True,
                max_bytes=-1,
                console=False,
            )

    def test_setup_logger_invalid_backup_count(self):
        with self.assertRaises(ValueError):
            setup_logger(
                loglevel=logging.DEBUG,
                file=True,
                rotating=True,
                backup_count=-1,
                console=False,
            )

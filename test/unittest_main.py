import unittest
import contextlib

from ..main import config, start_selenium

class SeleniumTest(unittest.TestCase):

    def test(self):
        driver = start_selenium(config.SERVER)
        with contextlib.closing(driver) as d:
            self.assertIsNotNone(d)
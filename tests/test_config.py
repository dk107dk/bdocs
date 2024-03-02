from bdocs.bdocs_config import BdocsConfig
import unittest
import logging

class ConfigTests(unittest.TestCase):


    def test_add_and_remove(self):
        logging.info(f"ConfigTests.test_add_and_remove")
        cfg = BdocsConfig()
        cfg.add_to_config("foo", "bar", "baz")
        cfg = BdocsConfig()
        items = cfg.get_items("foo")
        logging.info(f"ConfigTests.test_add_and_remove: items: {items}")
        self.assertEqual( len(items), 1, msg="must be 1 item in section foo" )
        cfg.remove_from_config("foo")
        cfg = BdocsConfig()
        items = cfg.get_items("foo")
        logging.info(f"ConfigTests.test_add_and_remove: items: {items}")
        self.assertEqual( len(items), 0, msg="must be 0 items in section foo" )





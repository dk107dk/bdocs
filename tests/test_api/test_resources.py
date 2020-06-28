from bdocs.bdocs_config import BdocsConfig
from api.resources import Resources
import unittest

class ResourcesTests(unittest.TestCase):

    noise = BdocsConfig().get("testing", "ResourcesTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "ResourcesTests") == "off"

    def test_get_resources(self):
        self._print(f"ResourcesTests.test_get_resources")
        if self._off(): return
        resources = Resources()


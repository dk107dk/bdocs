from cdocs.cdocs import Cdocs
import unittest
from bdocs.bdocs_config import BdocsConfig

PATH = "/Users/davidkershaw/dev/bdocs/server/docs"
ROOTNAME = "apiui"
ROOT = PATH + "/" + ROOTNAME

class ApiUiTests(unittest.TestCase):
    """
    WARNING: this test class doesn't do anything useful yet. leave it off.
    """

    noise = BdocsConfig().get("testing", "ApiUiTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def off(self) -> bool:
        return BdocsConfig().get("testing", "ApiUiTests") == "off"

    def test_index(self):
        self._print(f"ApiUiTests.test_index")
        if self.off(): return
        cdocs = Cdocs(ROOT)
        doc = cdocs.get_doc("/v1/index.html")
        self._print(f"ApiUiTests.test_index: doc: {doc}")

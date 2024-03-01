from bdocs.simple_rotater import SimpleRotater
import unittest
import os
import shutil
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
from bdocs.bdocs_config import BdocsConfig
from cdocs.contextual_docs import FilePath

BASE:FilePath = "/Users/davidkershaw/dev/bdocs/server"

class RotateTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setting up RotateTests")
        BdocsConfig.setTesting()

    noise = BdocsConfig().get("testing", "RotateTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "RotateTests") == "off"

    def test_rotate_file(self):
        self._print(f"RotateTests.test_rotate")
        if self._off(): return
        bdocs = Bdocs(BASE+ "/docs/example")
        metadata = BuildingMetadata()
        r = SimpleRotater(metadata, bdocs)
        dirname = os.getcwd() +"/tests/test_resources/"
        filename = dirname + "rotateme.zip"
        self._print(f"RotateTests.test_rotate: filename: {filename}")
        newname = "__rotateme.zip"
        newfile = dirname + newname
        shutil.copyfile(filename, newfile )
        rotatedto = r.rotate(newfile)
        self.assertEqual(True, os.path.exists(rotatedto), msg=f"test_rotate: {rotatedto} must exist")
        self.assertEqual(False, os.path.exists(newfile), msg=f"test_rotate: {newfile} must not exist")
        shutil.rmtree( os.path.join(dirname, "." + newname) )



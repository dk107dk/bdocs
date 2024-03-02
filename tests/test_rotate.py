from bdocs.simple_rotater import SimpleRotater
import unittest
import os
import shutil
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
from cdocs.contextual_docs import FilePath
import logging

class RotateTests(unittest.TestCase):



    def test_rotate_file(self):
        logging.info(f"RotateTests.test_rotate")
        bdocs = Bdocs("docs/example")
        metadata = BuildingMetadata()
        r = SimpleRotater(metadata, bdocs)
        dirname = os.getcwd() +"/tests/test_resources/"
        filename = dirname + "rotateme.zip"
        logging.info(f"RotateTests.test_rotate: filename: {filename}")
        newname = "__rotateme.zip"
        newfile = dirname + newname
        shutil.copyfile(filename, newfile )
        rotatedto = r.rotate(newfile)
        self.assertEqual(True, os.path.exists(rotatedto), msg=f"test_rotate: {rotatedto} must exist")
        self.assertEqual(False, os.path.exists(newfile), msg=f"test_rotate: {newfile} must not exist")
        shutil.rmtree( os.path.join(dirname, "." + newname) )



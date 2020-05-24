from bdocs.simple_rotater import SimpleRotater
import unittest
import os
import shutil

class RotateTests(unittest.TestCase):

    def test_rotate_file(self):
        #print(f"RotateTests.test_rotate")
        r = SimpleRotater()
        dirname = os.getcwd() +"/tests/resources/"
        filename = dirname + "rotateme.zip"
        #print(f"RotateTests.test_rotate: filename: {filename}")
        newname = "__rotateme.zip"
        newfile = dirname + newname
        shutil.copyfile(filename, newfile )
        rotatedto = r.rotate(newfile)
        self.assertEqual(True, os.path.exists(rotatedto), msg=f"test_rotate: {rotatedto} must exist")
        self.assertEqual(False, os.path.exists(newfile), msg=f"test_rotate: {newfile} must not exist")
        shutil.rmtree( os.path.join(dirname, "." + newname) )



from bdocs.git.git_rooter import GitRooter
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
import os
import unittest

PATH = "/Users/davidkershaw/dev/bdocs/docs"
ROOTNAME = "git_test"
ROOT = PATH + "/" + ROOTNAME

class GitTests(unittest.TestCase):

    noise = True
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def test_init(self):
        self._print(f"GitTests.test_init")
        metadata = BuildingMetadata()
        bdocs = Bdocs(ROOT)
        if not os.path.exists(bdocs.docs_root):
            os.mkdir(bdocs.docs_root)
        git_rooter = GitRooter(metadata, bdocs)
        bdocs.rooter = git_rooter
        bdocs.init_root()
        exist = os.path.exists( bdocs.docs_root)
        self.assertEqual(exist, True, msg=f"new root at {bdocs.docs_root} must exist")
        exist = os.path.exists( bdocs.docs_root + "/.git")
        self.assertEqual(exist, True, msg=f"new git dir at {bdocs.docs_root + '/.git'} must exist")
        bdocs.delete_root()
        exist = os.path.exists( bdocs.docs_root)
        self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")



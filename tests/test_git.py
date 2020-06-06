from bdocs.git.git_rooter import GitRooter
from bdocs.git.git_writer import GitWriter
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
from cdocs.cdocs import Cdocs
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

    def test_put(self):
        self._print(f"GitTests.test_put")
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH + "/git", metadata)
        git_rooter = GitRooter(metadata, bdocs)
        git_writer = GitWriter(metadata, bdocs)
        bdocs.rooter = git_rooter
        bdocs.writer = git_writer
        if not os.path.exists(bdocs.docs_root):
            os.mkdir(bdocs.docs_root)
            bdocs.init_root()
        doctext = "adding to git"
        bdocs.put_doc("/app/git_test", doctext )
        cdocs = Cdocs(PATH + "/git")
        doc = cdocs.get_doc("/app/git_test")
        self.assertEqual(doctext, doc, msg=f"{doc} must equal {doctext}")
        bdocs.delete_doc("/app/git_test")
        doc = cdocs.get_doc("/app/git_test")
        self.assertIsNone(doc, msg=f"{doc} must be none")
        if False:
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")





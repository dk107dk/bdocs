from bdocs.git.git_rooter import GitRooter
from bdocs.git.git_writer import GitWriter
from bdocs.git.git_deleter import GitDeleter
from bdocs.git.git_mover import GitMover
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
from bdocs.file_util import FileUtil
from bdocs.git.git_util import GitUtil
from cdocs.cdocs import Cdocs
import os
import unittest
from dulwich.objects import Blob
import time

PATH = "/Users/davidkershaw/dev/bdocs/docs"
ROOTNAME = "git_test"
ROOT = PATH + "/" + ROOTNAME

class GitTests(unittest.TestCase):

    noise = False
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return True

    def test_init(self):
        self._print(f"GitTests.test_init")
        if self._off(): return
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
        if self._off(): return
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
        if True:
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")

    def test_put_put(self):
        self._print(f"GitTests.test_put_put")
        if self._off(): return
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
        #
        # write. sleep to help make the walker entries more clear.
        #
        self._print(f"GitTests.test_put_put....sleeping....\n")
        time.sleep(.5)
        #
        # second write
        #
        doctext2 = "adding more to git"
        bdocs.put_doc("/app/git_test", doctext2 )
        self._print(f"GitTests.test_put_put....sleeping....\n")
        time.sleep(.5)
        #
        # third write
        #
        doctext3 = "adding to git again"
        bdocs.put_doc("/app/git_test", doctext3 )
        util = GitUtil(metadata, bdocs)
        entries = util.get_log_entries(paths=[b'app/git_test.xml'])
        self._print(f"GitTests.test_put_put: entries: {entries}")
        content = []
        for entry in entries:
            _ = util.get_content(entry)
            content.append(_)
            self._print(f"GitTests.test_put_put: _: {_}")
        self.assertEqual(content[0]["app/git_test.xml"].decode("utf-8"), doctext3, msg=f"{content[0]} must equal {doctext3}")
        self.assertEqual(content[1]["app/git_test.xml"].decode("utf-8"), doctext2, msg=f"{content[1]} must equal {doctext2}")
        self.assertEqual(content[2]["app/git_test.xml"].decode("utf-8"), doctext, msg=f"{content[2]} must equal {doctext}")
        #
        # check version
        #
        cdocs = Cdocs(PATH + "/git")
        doc = cdocs.get_doc("/app/git_test")
        self.assertEqual(doctext3, doc, msg=f"{doc} must equal {doctext3}")
        if True:
            bdocs.delete_doc("/app/git_test")
            doc = cdocs.get_doc("/app/git_test")
            self.assertIsNone(doc, msg=f"{doc} must be none")
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")

    def test_delete(self):
        self._print(f"GitTests.test_delete")
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH + "/git", metadata)
        git_rooter = GitRooter(metadata, bdocs)
        git_writer = GitWriter(metadata, bdocs)
        git_deleter = GitDeleter(metadata, bdocs)
        bdocs.rooter = git_rooter
        bdocs.writer = git_writer
        bdocs.deleter = git_deleter
        if not os.path.exists(bdocs.docs_root):
            os.mkdir(bdocs.docs_root)
            self._print(f"GitTests.test_delete: initing root: {bdocs.docs_root}")
            bdocs.init_root()
        doctext = "adding to git"
        bdocs.put_doc("/app/git_test", doctext )
        doctext2 = "adding to git"
        bdocs.put_doc("/app/git_test/fish", doctext2 )
        filepath = bdocs.get_dir_for_docpath("/app/git_test")
        chkpath = PATH + "/git/app/git_test"
        exists = os.path.exists(chkpath)
        self.assertEqual( exists, True, msg=f"chkpath {chkpath} must exist")
        self._print(f"GitTests.test_delete: {chkpath} exists: {exists}")
        self.assertEqual( exists, True, msg=f"{chkpath} must exist")
        self.assertEqual( filepath, chkpath, msg=f"filepath {filepath} must equal {chkpath}")
        #
        # test get file names -- this probably belongs somewhere other than GitDeleter
        #
        fileutil = FileUtil( metadata, bdocs )
        filepaths = fileutil.get_file_names(filepath)
        self._print(f"GitTests.test_delete: filepaths: {filepaths}")
        self.assertIn('/Users/davidkershaw/dev/bdocs/docs/git/app/git_test/fish.xml', \
                       filepaths, msg=f"must have '/Users/davidkershaw/dev/bdocs/docs/git/app/git_test/fish.xml'")
        #
        # do the delete
        #
        bdocs.delete_doc_tree("/app/git_test")
        bdocs.delete_doc("/app/git_test.xml")
        if True:
            cdocs = Cdocs(PATH + "/git")
            doc = cdocs.get_doc("/app/git_test")
            self.assertIsNone(doc, msg=f"{doc} must be none")
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")

    def test_move(self):
        self._print(f"GitTests.test_move")
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH + "/git", metadata)
        git_rooter = GitRooter(metadata, bdocs)
        git_writer = GitWriter(metadata, bdocs)
        git_deleter = GitDeleter(metadata, bdocs)
        git_mover = GitMover(metadata, bdocs)
        bdocs.rooter = git_rooter
        bdocs.writer = git_writer
        bdocs.deleter = git_deleter
        bdocs.mover = git_mover
        if not os.path.exists(bdocs.docs_root):
            os.mkdir(bdocs.docs_root)
            self._print(f"GitTests.test_move: initing root: {bdocs.docs_root}")
            bdocs.init_root()
        doctext = "adding to git"
        bdocs.put_doc("/app/git_test", doctext )
        filepath = bdocs.get_dir_for_docpath("/app/git_test")
        chkpath = filepath + ".xml"
        exists = os.path.exists(chkpath)
        self.assertEqual( exists, True, msg=f"chkpath {chkpath} must exist")
        self._print(f"GitTests.test_move: {chkpath} exists: {exists}")
        bdocs.move_doc( "/app/git_test", "/app/git_move" )
        util = GitUtil(metadata, bdocs)
        self._print(f"GitTests.test_move: log is: {util.get_log()}")
        #
        # check the remove commit
        #
        self._print("GitTests.test_move: checking remove commit")
        entries = util.get_log_entries(paths=[b'app/git_test.xml'])
        for entry in entries:
            for change in entry.changes():
                self._print(f"GitTests.test_move:   > new.path: {change.new.path}")
                self._print(f"GitTests.test_move:   > old.path: {change.old.path}\n")
        self.assertIsNone( entries[0].changes()[0].new.path, msg=f"new.path must be None")
        self.assertEqual( entries[0].changes()[0].old.path, b'app/git_test.xml', msg=f"old.path must be b'app/git_test.xml'")
        self.assertIsNone( entries[1].changes()[0].old.path, msg=f"old.path must be None")
        self.assertEqual( entries[1].changes()[0].new.path, b'app/git_test.xml', msg=f"new.path must be b'app/git_test.xml'")
        #
        # check the move commit
        #
        self._print("GitTests.test_move: checking move commit")
        entries = util.get_log_entries(paths=[b'app/git_move.xml'])
        for entry in entries:
            for change in entry.changes():
                self._print(f"GitTests.test_move:   > new.path: {change.new.path}")
                self._print(f"GitTests.test_move:   > old.path: {change.old.path}\n")
        self.assertIsNone( entries[0].changes()[0].old.path, msg=f"new.path must be None")
        self.assertEqual( entries[0].changes()[0].new.path, b'app/git_move.xml', msg=f"new.path must be b'app/git_move.xml'")
        if True:
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")

    def test_copy(self):
        self._print(f"GitTests.test_copy")
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH + "/git", metadata)
        git_rooter = GitRooter(metadata, bdocs)
        git_writer = GitWriter(metadata, bdocs)
        git_deleter = GitDeleter(metadata, bdocs)
        git_mover = GitMover(metadata, bdocs)
        bdocs.rooter = git_rooter
        bdocs.writer = git_writer
        bdocs.deleter = git_deleter
        bdocs.mover = git_mover
        if not os.path.exists(bdocs.docs_root):
            os.mkdir(bdocs.docs_root)
            self._print(f"GitTests.test_copy: initing root: {bdocs.docs_root}")
            bdocs.init_root()
        doctext = "adding to git"
        bdocs.put_doc("/app/git_test", doctext )
        filepath = bdocs.get_dir_for_docpath("/app/git_test")
        chkpath = filepath + ".xml"
        exists = os.path.exists(chkpath)
        self.assertEqual( exists, True, msg=f"chkpath {chkpath} must exist")
        self._print(f"GitTests.test_move: {chkpath} exists: {exists}")
        bdocs.copy_doc( "/app/git_test", "/app/git_copy" )
        util = GitUtil(metadata, bdocs)
        self._print(f"GitTests.test_copy: log is: {util.get_log()}")
        #
        # check the add commit
        #
        self._print("GitTests.test_copy: checking add commit")
        entries = util.get_log_entries(paths=[b'app/git_test.xml'])
        for entry in entries:
            for change in entry.changes():
                self._print(f"GitTests.test_copy:   > new.path: {change.new.path}")
                self._print(f"GitTests.test_copy:   > old.path: {change.old.path}\n")
        self.assertEqual( len(entries), 1, msg=f"log entries for b'app/git_test.xml' must be 1")
        self.assertIsNone( entries[0].changes()[0].old.path, msg=f"old.path must be None")
        self.assertEqual( entries[0].changes()[0].new.path, b'app/git_test.xml', msg=f"new.path must be b'app/git_test.xml'")
        #
        # check the copy commit
        #
        self._print("GitTests.test_copy: checking copy commit")
        entries = util.get_log_entries(paths=[b'app/git_copy.xml'])
        for entry in entries:
            for change in entry.changes():
                self._print(f"GitTests.test_copy:   > new.path: {change.new.path}")
                self._print(f"GitTests.test_copy:   > old.path: {change.old.path}\n")
        self.assertEqual( len(entries), 1, msg=f"log entries for b'app/git_copy.xml' must be 1")
        self.assertIsNone( entries[0].changes()[0].old.path, msg=f"old.path must be None")
        self.assertEqual( entries[0].changes()[0].new.path, b'app/git_copy.xml', msg=f"new.path must be b'app/git_copy.xml'")
        if True:
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")





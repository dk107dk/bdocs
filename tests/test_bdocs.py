from bdocs.bdocs import Bdocs
from bdocs.printer import Printer
from bdocs.building_metadata import BuildingMetadata
from cdocs.cdocs import Cdocs
from cdocs.cdocs import BadDocPath
from cdocs.contextual_docs import DocPath, FilePath
import unittest
import os
import shutil
import logging

BASE:FilePath = "/Users/davidkershaw/dev/bdocs"
PATH:FilePath = BASE + "/docs/example"
TMP:FilePath = BASE + "/tmp"
HOME:DocPath = "/app/home"


import inspect

class BdocsTests(unittest.TestCase):

    def _debug(self):
        self.logger.setLevel(level=logging.DEBUG)
        self.logger.debug("SET THE LEVEL TO DEBUG")

    def _warning(self):
        self.logger.setLevel(level=logging.WARNING)
        self.logger.warning("SET THE LEVEL TO WARNING")

    logger = logging.getLogger('')

    noise = False
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def test_zip_doc_tree(self):
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        azip = bdocs.zip_doc_tree()
        b = os.path.exists(azip)
        self.assertEqual(b, True, msg=f'{azip} must exist')
        if b:
            os.remove(azip)

    def test_move_doc(self):
        self._print(f"BdocsTests.test_move_doc")
        cdocs = Cdocs(PATH)
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        moving = "I'm moving!"
        fromdoc = "/app/home/teams#added_doc"
        todoc = "/app/home/teams#moved_doc"
        bdocs.put_doc(fromdoc, moving)
        doc = cdocs.get_doc(fromdoc)
        self.assertIsNotNone(doc, msg=f"{doc} at {fromdoc} must be there")
        bdocs.move_doc(fromdoc, todoc)
        doc = cdocs.get_doc(fromdoc)
        self.assertIsNone(doc, msg=f"{doc} at {fromdoc} must be none")
        doc = cdocs.get_doc(todoc)
        moved = doc.find(moving)
        self.assertNotEqual(moved,-1, msg="{doc} must have {moving}")
        bdocs.delete_doc(todoc)
        doc = cdocs.get_doc(todoc)
        self.assertIsNone(doc, msg=f"{doc} at {todoc} must be none")

    def test_copy_doc(self):
        self._print(f"BdocsTests.test_copy_doc")
        cdocs = Cdocs(PATH)
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        copying = "I'm a copy!"
        fromdoc = "/app/home/teams#source_doc"
        todoc = "/app/home/teams#copyed_doc"
        bdocs.put_doc(fromdoc, copying)
        doc = cdocs.get_doc(fromdoc)
        self.assertIsNotNone(doc, msg=f"{doc} at {fromdoc} must be there")
        bdocs.copy_doc(fromdoc, todoc)
        doc = cdocs.get_doc(fromdoc)
        self.assertIsNotNone(doc, msg=f"{doc} at {fromdoc} must still be there")
        doc = cdocs.get_doc(todoc)
        copied = doc.find(copying)
        self.assertNotEqual(copied,-1, msg="{doc} must have {copying}")
        bdocs.delete_doc(todoc)
        doc = cdocs.get_doc(todoc)
        self.assertIsNone(doc, msg=f"{doc} at {todoc} must be none")
        bdocs.delete_doc(fromdoc)
        doc = cdocs.get_doc(fromdoc)
        self.assertIsNone(doc, msg=f"{doc} at {fromdoc} must be none")

    def test_get_doc_root_path(self):
        self._print(f"BdocsTests.test_get_doc_root_path")
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        path = bdocs.get_docs_root()
        self._print(f"test_get_doc_root_path: docs root is {path}")
        self.assertTrue( os.path.exists(path), msg="docs root must exsit" )
        self.assertEqual(path, PATH)

    def test_put_and_delete_doc(self):
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        home = "I'm home!"
        bdocs.put_doc(HOME, home)
        cdocs = Cdocs(PATH)
        doc = cdocs.get_doc(HOME)
        self.assertEqual(home, doc, msg=f"{doc} must equal {home}")
        bdocs.delete_doc(HOME)
        doc = cdocs.get_doc(HOME)
        self.assertIsNone(doc, msg=f"{doc} must be none")

    def test_delete_dir(self):
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        cdocs = Cdocs(PATH)
        #self._debug()
        filepath = bdocs.get_dir_for_docpath(HOME)
        apath = filepath + "/deleteme"
        os.mkdir(apath)
        with open(apath + '/deleteme.xml', 'w') as fp:
            pass
        bdocs.delete_doc_tree(HOME+"/deleteme")
        filepath = bdocs.get_dir_for_docpath(HOME+"/deleteme")
        b = os.path.exists(filepath)
        self.assertEqual(b, False, msg=f'{filepath} must not exist')
        #self._warning()

    def test_get_doc_tree(self):
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH + '/app/home/teams/todos', metadata)
        tree = bdocs.get_doc_tree()
        self.assertIn( 'assignee', tree, msg=f'tree must include "assignee"' )
        self.assertEqual( len(tree), 3, msg=f'tree must have three keys: {tree}')

    def test_get_docs_with_titles(self):
        metadata = BuildingMetadata()
        bdocs = Bdocs(PATH, metadata)
        docs:doc[str,DocPath] = bdocs.get_docs_with_titles("/app/home/teams/todos/assignee")
        self._print(f"test_get_docs_with_titles: all labeled docs: {docs}")
        self.assertEqual(len(docs), 4, msg=f'docs must have four docpath with titles: {docs}')
        found_app = False
        found_assignee = False
        found_new = False
        found_edit = False
        for k,v in docs.items():
            if v == '/app':
                found_app = True
            elif v == '/app/home/teams/todos/assignee':
                found_assignee = True
            elif v == '/app/home/teams/todos/assignee#new_assignee':
                found_new = True
            elif v == '/app/home/teams/todos/assignee#edit_assignee':
                found_edit = True
        self.assertEqual(found_app, True, msg="didn't find app")
        self.assertEqual(found_assignee, True, msg="didn't find assignee")
        self.assertEqual(found_new, True, msg="didn't find new")
        self.assertEqual(found_edit, True, msg="didn't find edit")




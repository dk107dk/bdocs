from bdocs.bdocs import Bdocs
from bdocs.printer import Printer
from cdocs.cdocs import Cdocs
from cdocs.cdocs import BadDocPath
from cdocs.contextual_docs import DocPath, FilePath
import unittest
import os
import shutil

BASE:FilePath = "/Users/davidkershaw/dev/bdocs"
PATH:FilePath = BASE + "/docs/example"
TMP:FilePath = BASE + "/tmp"
HOME:DocPath = "/app/home"

class BdocsTests(unittest.TestCase):

    def test_get_doc_root_path(self):
        #print(f"BdocsTests.test_get_doc_root_path")
        bdocs = Bdocs(PATH)
        path = bdocs.get_docs_root()
        #print(f"test_get_doc_root_path: docs root is {path}")
        self.assertTrue( os.path.exists(path), msg="docs root must exsit" )
        self.assertEqual(path, PATH)

    def test_put_and_delete_doc(self):
        bdocs = Bdocs(PATH)
        home = "I'm home!"
        bdocs.put_doc(HOME, home)
        cdocs = Cdocs(PATH)
        doc = cdocs.get_doc(HOME)
        self.assertEqual(home, doc, msg=f"{doc} must equal {home}")
        bdocs.delete_doc(HOME)
        doc = cdocs.get_doc(HOME)
        self.assertIsNone(doc, msg=f"{doc} must be none")

    def test_delete_dir(self):
        bdocs = Bdocs(PATH)
        cdocs = Cdocs(PATH)
        filepath = bdocs.get_dir_for_docpath(HOME)
        apath = filepath + "/deleteme"
        os.mkdir(apath)
        with open(apath + '/deleteme.xml', 'w') as fp:
            pass
        bdocs.delete_doc_tree(HOME+"/deleteme")
        filepath = bdocs.get_dir_for_docpath(HOME+"/deleteme")
        b = os.path.exists(filepath)
        self.assertEqual(b, False, msg=f'{filepath} must not exist')

    def test_get_doc_tree(self):
        bdocs = Bdocs(PATH + '/app/home/teams/todos')
        tree = bdocs.get_doc_tree()
        #Printer().print_tree(tree)
        self.assertIn( 'assignee', tree, msg=f'tree must include "assignee"' )
        self.assertEqual( len(tree), 3, msg=f'tree must have three keys: {tree}')

    def test_zip_doc_tree(self):
        bdocs = Bdocs(PATH)
        azip = bdocs.zip_doc_tree()
        b = os.path.exists(azip)
        self.assertEqual(b, True, msg=f'{azip} must exist')
        if b:
            os.remove(azip)

    def test_unzip_doc_tree(self):
        bdocs = Bdocs(PATH)
        shutil.copyfile(BASE+"/tests/resources/test.zip", BASE+"/tests/resources/____.zip" )
        bdocs.unzip_doc_tree( BASE+"/tests/resources/____.zip" )
        b = os.path.exists( BASE + "/docs/test")
        self.assertEqual(b, True, msg=f'{BASE + "/docs/test"} must exist')
        if b:
            shutil.rmtree(BASE + "/docs/test")
            bdocs.config.remove_from_config("docs", "test")

    def test_get_docs_with_titles(self):
        bdocs = Bdocs(PATH)
        docs:doc[str,DocPath] = bdocs.get_docs_with_titles("/app/home/teams/todos/assignee")
        #print(f"test_get_docs_with_titles: all labeled docs: {docs}")
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




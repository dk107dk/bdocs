from bdocs.bdocs import Bdocs
from cdocs.cdocs import Cdocs
from cdocs.cdocs import BadDocPath
from cdocs.contextual_docs import DocPath, FilePath
import unittest
import os

PATH:FilePath = "/Users/davidkershaw/dev/bdocs/docs/example"
HOME:DocPath = "/app/home"

class BdocsTests(unittest.TestCase):

    def test_get_doc_root_path(self):
        print(f"BdocsTests.test_get_doc_root_path")
        bdocs = Bdocs(PATH)
        path = bdocs.get_docs_root()
        print(f"test_get_doc_root_path: docs root is {path}")
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
        # should return: {'assignee': 'assignee.xml', 'tokens': 'tokens.json'}
        self.assertIn( 'assignee', tree, msg=f'tree must include "assignee"' )
        self.assertEqual( len(tree), 2, msg=f'tree must have two keys')

    def test_zip_doc_tree(self):
        bdocs = Bdocs(PATH)
        azip = bdocs.zip_doc_tree()
        b = os.path.exists(azip)
        self.assertEqual(b, True, msg=f'{azip} must exist')
        if b:
            os.remove(azip)


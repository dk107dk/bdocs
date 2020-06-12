import unittest
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
from cdocs.cdocs import Cdocs
from bdocs.search.whoosh_indexer import WhooshIndexer
from bdocs.search.whoosh_searcher import WhooshSearcher
from bdocs.searcher import Query
import os

PATH = "/Users/davidkershaw/dev/bdocs/docs"
ROOTNAME = "search_test"
ROOT = PATH + "/" + ROOTNAME

class SearchTests(unittest.TestCase):

    noise = True
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return False

    def test_index(self):
        self._print(f"SearchTests.test_index")
        #if self._off(): return
        metadata = BuildingMetadata()
        bdocs = Bdocs(ROOT, metadata)
        win = WhooshIndexer(metadata, bdocs)
        ws = WhooshSearcher(metadata, bdocs)
        bdocs.indexer = win
        bdocs.searcher = ws
        if not os.path.exists(bdocs.docs_root):
            os.mkdir(bdocs.docs_root)
            bdocs.init_root()
        doctext = "please index me"
        docpath = "/app/index_test"
        bdocs.put_doc(docpath, doctext)
        cdocs = Cdocs(bdocs.get_doc_root())
        doc = cdocs.get_doc(docpath)
        self.assertEqual(doctext, doc, msg=f"{doc} must equal {doctext}")


        query = Query("please")
        doc = bdocs.searcher.find_docs(query)
        print(f"SearchTests.test_index: the query returned {doc}")

        bdocs.delete_doc(docpath)
        doc = cdocs.get_doc(docpath)
        self.assertIsNone(doc, msg=f"{doc} must be none")
        if False:
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")
            index_root = win.get_index_root()
            win.delete_index()
            exist = os.path.exists( index_root)
            self.assertEqual(exist, False, msg=f"index root at {index_root} must no longer exist")


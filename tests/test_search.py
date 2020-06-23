import unittest
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs_config import BdocsConfig
from bdocs.bdocs import Bdocs
from cdocs.cdocs import Cdocs
from bdocs.search.whoosh_indexer import WhooshIndexer
from bdocs.search.whoosh_searcher import WhooshSearcher
from bdocs.searcher import Query
from bdocs.search.index_doc import IndexDoc
import os

PATH = "/Users/davidkershaw/dev/bdocs/server/docs"
ROOTNAME = "search_test"
ROOT = PATH + "/" + ROOTNAME

class SearchTests(unittest.TestCase):

    noise = BdocsConfig().get("testing", "SearchTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "SearchTests") == "off"

    def test_index_doc(self):
        self._print(f"SearchTests.test_index_doc")
        if self._off(): return
        json = {}
        json["root"] = "root"
        json["path"] = "path"
        json["paths"] = "paths"
        """author
        contributors
        content
        title
        created
        updated"""
        doc = IndexDoc(json)
        self.assertEqual(doc.root, "root", msg=f"doc.root must == 'root'")
        self.assertEqual(doc.path, "path", msg=f"doc.path must == 'path'")
        self.assertEqual(doc.paths, "paths", msg=f"doc.paths must == 'paths'")
        self.assertIsNone(doc.author, msg=f"doc.author must be None")
        self.assertIsNone(doc.content, msg=f"doc.content must be None")

    def test_index(self):
        self._print(f"SearchTests.test_index")
        if self._off(): return
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
        docs = bdocs.searcher.find_docs(query)
        print(f"SearchTests.test_index: find: the query returned {docs}")
        self.assertIn(docpath, docs, msg=f"query must return {docpath}")

        docs = bdocs.searcher.find_docs_with_metadata(query)
        print(f"SearchTests.test_index: find meta: the query returned {docs}")
        for doc in docs:
            print(f"SearchTests.test_index: metadata: {doc}")
        self.assertEqual( len(docs), 1, msg=f"number of docs found must be 1, not {len(docs)} was last run successful?")

        bdocs.delete_doc(docpath)
        doc = cdocs.get_doc(docpath)
        self.assertIsNone(doc, msg=f"{doc} must be none")

        docs = bdocs.searcher.find_docs(query)
        print(f"SearchTests.test_index: find: the query returned {docs}")
        self.assertEqual(len(docs), 0, msg=f"query must return nothing")

        if True:
            bdocs.delete_root()
            exist = os.path.exists( bdocs.docs_root)
            self.assertEqual(exist, False, msg=f"new root at {bdocs.docs_root} must no longer exist")
            index_root = win.get_index_root()
            win.delete_index()
            exist = os.path.exists( index_root)
            self.assertEqual(exist, False, msg=f"index root at {index_root} must no longer exist")


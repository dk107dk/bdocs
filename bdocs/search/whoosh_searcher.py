from cdocs.contextual_docs import JsonDict, DocPath
from bdocs.searcher import Searcher, Query
from bdocs.search.whoosh_index import WhooshIndex
from bdocs.search.index_doc import IndexDoc
from bdocs.building_metadata import BuildingMetadata
from whoosh.qparser import QueryParser
from whoosh import index
from typing import List, Dict, Any
import logging

class WhooshSearcher(WhooshIndex, Searcher):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        super().__init__()
        self._metadata = metadata
        self._bdocs = bdocs
        self._check_index()

    def find_docs(self, query:Query, root_doc_paths:bool=False) -> List[DocPath]:
        """ if root_doc_paths the results will be RootDocPath, rather than DocPath """
        ix = index.open_dir(self.get_index_root())
        with (ix.searcher()) as searcher:
            q = QueryParser("content", self._schema).parse(query._query)
            results = searcher.search(q, terms=True)
            paths = []
            for hit in results:
                logging.info(f"WhooshSearcher.find_docs: hit: {type(hit)}, with score: {hit.score} and terms: {hit.matched_terms()}")
                path = hit["path"]
                if root_doc_paths:
                    path = self._bdocs.root_name + ":" + path
                paths.append(path)
            return paths

    def find_docs_with_metadata(self, query:Query) -> List[JsonDict]:
        ix = index.open_dir(self.get_index_root())
        with (ix.searcher()) as searcher:
            q = QueryParser("content", self._schema).parse(query._query)
            results = searcher.search(q, terms=True)
            docs:List[Dict[str,Any]] = []
            for hit in results:
                logging.info(f"WhooshSearcher.find_docs_with_metadata: hit: {type(hit)}, with score: {hit.score} and terms: {hit.matched_terms()}")
                m = hit.fields()
                doc = IndexDoc(m)
                docs.append(m)
            return docs


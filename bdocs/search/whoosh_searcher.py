from cdocs.contextual_docs import JsonDict, DocPath
from bdocs.searcher import Searcher, Query
from bdocs.indexer import Index
from bdocs.search.whoosh_index import WhooshIndex
from bdocs.search.whoosh_indexer import WhooshIndexer
from bdocs.building_metadata import BuildingMetadata
from whoosh.qparser import QueryParser
from typing import List

class WhooshSearcher(WhooshIndex, Searcher):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        super().__init__()
        self._metadata = metadata
        self._bdocs = bdocs
        self._check_index()

    def find_docs(self, query:Query) -> List[DocPath]:
        with self._get_index().searcher() as searcher:
            q = QueryParser("content", self._schema).parse(query._query)
            results = searcher.search(q, terms=True)
            for r in results:
                print (r, r.score)
                # Was this results object created with terms=True?
                if results.has_matched_terms():
                    # What terms matched in the results?
                    print(results.matched_terms())
            for hit in results:
                print(hit.matched_terms())

            return []

    def find_docs_with_metadata(self, query:Query) -> List[JsonDict]:
        pass


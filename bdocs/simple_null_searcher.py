from cdocs.contextual_docs import JsonDict, DocPath
from bdocs.searcher import Searcher, Query
from typing import List

class SimpleNullSearcher(Searcher):

    def __init__(self, metadata, bdocs):
        pass

    def find_docs(self, query:Query) -> List[DocPath]:
        pass

    def find_docs_with_metadata(self, query:Query) -> List[JsonDict]:
        pass


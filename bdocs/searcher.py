import abc
from cdocs.contextual_docs import JsonDict, DocPath
from typing import List, Optional

class Query(object):

    def __init__(self, query:Optional[str]=None):
        self._query:str = query

class Searcher(metaclass=abc.ABCMeta):
    """
    searcher knows how to find docs.
    """

    @abc.abstractmethod
    def find_docs(self, query:Query) -> List[DocPath]:
        pass

    @abc.abstractmethod
    def find_docs_with_metadata(self, query:Query) -> List[JsonDict]:
        pass


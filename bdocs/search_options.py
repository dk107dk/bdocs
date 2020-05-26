from cdocs.contextual_docs import DocPath
from typing import List

class SearchOptions(object):

    def __init__(self):
        self._lookdown = True
        self._lookup = False
        self._include_starting_path = False
        self._exclude_paths:List[DocPath] = []

    @property
    def lookdown(self):
        return self._lookdown

    @property
    def lookup(self):
        return self._lookup

    @property
    def include_starting_path(self):
        return self._include_starting_path

    @property
    def exclude_paths(self) -> List[DocPath]:
        return self._exclude_paths


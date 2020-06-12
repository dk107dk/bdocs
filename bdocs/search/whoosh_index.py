import os
from whoosh import index
from whoosh.fields import Schema,  TEXT, ID
from bdocs.indexer import Index

class WhooshIndex(Index):

    def __init__(self):
        self._schema = Schema(path=ID(stored=True), content=TEXT(stored = True), title=TEXT(stored=True))


    def _get_index(self):
        try:
            return index.open_dir(self.get_index_root())
        except:
            return index.create_in(self.get_index_root(), self._schema)



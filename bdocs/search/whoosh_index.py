import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME, KEYWORD
from bdocs.search.index import Index

class WhooshIndex(Index):

    def __init__(self):
        self._schema = Schema(\
                        root=ID(stored=True),\
                        path=ID(stored=True), \
                        paths=ID, \
                        author=ID(stored=True), \
                        contributors=KEYWORD(stored=True), \
                        content=TEXT, \
                        title=TEXT(stored=True), \
                        created=DATETIME, \
                        updated=DATETIME \
                        )


    def _get_index(self):
        try:
            return index.open_dir(self.get_index_root())
        except:
            return index.create_in(self.get_index_root(), self._schema)



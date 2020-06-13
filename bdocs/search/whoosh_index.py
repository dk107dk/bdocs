import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME, KEYWORD
from whoosh.index import EmptyIndexError
from bdocs.search.index import Index
import logging
import shutil

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


    def _assure_index(self):
        logging.info(f"WhooshIndex._assure_index: for {self}")
        try:
            xi = index.open_dir(self.get_index_root())
            logging.info(f"WhooshIndex._assure_index: index at {self.get_index_root()} exists")
        except EmptyIndexError as e:
            logging.info(f"WhooshIndex._assure_index: couldn't open index at {self.get_index_root()}, try create new index. {e}")
            try:
                logging.info(f"WhooshIndex._assure_index: deleting index root before creating it")
                shutil.rmtree(self.get_index_root())
                logging.info(f"WhooshIndex._assure_index: creating index root dir before creating index")
                os.mkdir(self.get_index_root())
            except Exception as e:
                pass
            index.create_in(self.get_index_root(), self._schema)



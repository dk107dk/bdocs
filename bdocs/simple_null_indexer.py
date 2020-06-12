from cdocs.contextual_docs import JsonDict, DocPath, Doc, FilePath
from bdocs.indexer import Indexer
from typing import Optional

class SimpleNullIndexer(Indexer):

    def __init__(self, metadata, bdocs):
        pass

    def index_doc(self, path:DocPath, doc:Doc, metadata:Optional[JsonDict]=None) -> None:
        pass

    def remove_doc(self, path:DocPath) -> None:
        pass

    def get_index_root(self) -> FilePath:
        return None


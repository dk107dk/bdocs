import abc
from cdocs.contextual_docs import JsonDict, DocPath, Doc, FilePath
from typing import Optional
import os
import shutil

class Index(metaclass=abc.ABCMeta):

    def _check_index(self):
        if not os.path.exists(self.get_index_root()):
            os.mkdir(self._index)
            self._get_index()

    def get_index_root(self):
        root = self._bdocs.get_doc_root()
        (base,_) = os.path.split(root)
        return os.path.join(base, '.'+_+"_index")

    def delete_index(self):
        root = self.get_index_root()
        shutil.rmtree(root)

    @abc.abstractmethod
    def _get_index(self):
        pass

class Indexer(metaclass=abc.ABCMeta):
    """
    indexer knows how to add docs to a search index.
    """

    @abc.abstractmethod
    def index_doc(self, path:DocPath, doc:Doc, metadata:Optional[JsonDict]=None) -> None:
        pass

    @abc.abstractmethod
    def remove_doc(self, path:DocPath) -> None:
        pass

    @abc.abstractmethod
    def get_index_root(self) -> FilePath:
        pass


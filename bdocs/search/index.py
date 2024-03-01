import abc
from cdocs.contextual_docs import FilePath
import os
import shutil
import logging

class Index(metaclass=abc.ABCMeta):
    """ implementations of Index must have self._bdocs """

    def _check_index(self) -> None:
        logging.info(f"Index._check_index: checking index for {self}")
        if not os.path.exists(self.get_index_root()):
            os.mkdir(self.get_index_root())
            self._assure_index()

    def get_index_root(self) -> FilePath:
        root = self._bdocs.get_doc_root()
        (base,_) = os.path.split(root)
        return os.path.join(base, '.'+_+"_index")

    def delete_index(self) -> None:
        root = self.get_index_root()
        shutil.rmtree(root)

    @abc.abstractmethod
    def _assure_index(self):
        pass


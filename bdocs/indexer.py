import abc
from cdocs.contextual_docs import JsonDict, DocPath, Doc, FilePath
from typing import Optional
import os
import shutil


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


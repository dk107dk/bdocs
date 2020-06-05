import abc
from typing import Union, Optional, Dict
from bdocs.search_options import SearchOptions
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict


class BuildingDocs(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_docs_root(self) -> FilePath:
        pass

    @abc.abstractmethod
    def put_doc(self, path:DocPath, doc:Union[bytes,Doc]) -> None:
        pass

    @abc.abstractmethod
    def move_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        pass

    @abc.abstractmethod
    def copy_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        pass

    @abc.abstractmethod
    def delete_doc(self, path:DocPath) -> None:
        pass

    @abc.abstractmethod
    def delete_doc_tree(self, path:DocPath) -> None:
        pass

    @abc.abstractmethod
    def get_dir_for_docpath(self, path:DocPath) -> FilePath:
        pass

    @abc.abstractmethod
    def doc_exists(self, path:DocPath) -> bool:
        pass

    @abc.abstractmethod
    def get_doc_tree(self) -> JsonDict:
        pass

    # belongs in cdocs
    @abc.abstractmethod
    def get_docs_with_titles(self, path:DocPath, options:Optional[SearchOptions]=None) -> Dict[str, DocPath]:
        pass

    @abc.abstractmethod
    def zip_doc_tree(self) -> FilePath:
        pass

    # this doesn't really belong here because each Bdocs has
    # its own root and shouldn't be messing around with unzipping
    # another root
    def unzip_doc_tree(self, zipfile:FilePath) -> None:
        pass



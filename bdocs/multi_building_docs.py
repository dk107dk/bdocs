import abc
from typing import Union, Optional, Dict, List
from bdocs.search_options import SearchOptions
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict

class MultiBuildingDocs(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def unzip_doc_tree(self, zipfile:FilePath) -> None:
        pass

    @abc.abstractmethod
    def get_root(self, rootname:str):  # cannot hint return type Bdocs because circular
        pass

    @abc.abstractmethod
    def join_trees(self, rootnames:List[str]) -> JsonDict:
        pass

    @abc.abstractmethod
    def list_trees(self, rootnames:List[str], add_root_names:bool=True ) -> List[str]:
        pass

    @abc.abstractmethod
    def put_doc(self, rootname:str, path:DocPath, doc:Union[bytes,Doc]) -> None:
        pass

    @abc.abstractmethod
    def move_doc(self, fromrootname:str, fromdoc:DocPath, torootname:str, todoc:DocPath) -> None:
        pass

    @abc.abstractmethod
    def copy_doc(self, fromrootname:str, fromdoc:DocPath, torootname:str, todoc:DocPath) -> None:
        pass

    @abc.abstractmethod
    def delete_doc(self, rootnames:List[str], path:DocPath) -> None:
        pass

    @abc.abstractmethod
    def delete_doc_tree(self, rootnames:List[str], path:DocPath) -> None:
        pass

    @abc.abstractmethod
    def get_dir_for_docpath(self, rootname:str, path:DocPath) -> FilePath:
        pass

    @abc.abstractmethod
    def doc_exists(self, rootnames:List[str], path:DocPath) -> bool:
        pass

    @abc.abstractmethod
    def get_doc_tree(self, rootname:str) -> JsonDict:
        pass

    @abc.abstractmethod
    def zip_doc_tree(self, rootname:str) -> FilePath:
        pass




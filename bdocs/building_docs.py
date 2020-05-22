import abc
from typing import Union
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict

class BuildingDocs(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_docs_root(self) -> FilePath:
        pass

    @abc.abstractmethod
    def put_doc(self, path:DocPath, doc:Union[bytes,Doc]) -> None:
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

    def get_doc_tree(self) -> JsonDict:
        pass


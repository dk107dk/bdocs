import abc
from cdocs.contextual_docs import Path


class Deleter(metaclass=abc.ABCMeta):
    """
    Deleter knows how to delete a path from a store. by default it
    deletes from the filesystem.
    """

    @abc.abstractmethod
    def delete(self, filepath:Path) -> None:
        pass

    @abc.abstractmethod
    def delete_doc_tree(self, filepath:Path) -> None:
        """
        some implementations may require this method
        be used to delete directory-like paths
        """
        pass

    def isdir(self, filepath:Path) -> bool:
        pass

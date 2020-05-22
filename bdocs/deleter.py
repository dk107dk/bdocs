import abc
from cdocs.contextual_docs import FilePath


class Deleter(metaclass=abc.ABCMeta):
    """
    Deleter knows how to delete a path from a store. by default it
    deletes from the filesystem.
    """

    @abc.abstractmethod
    def delete(self, filepath:FilePath) -> None:
        pass

    def isdir(self, filepath:FilePath) -> bool:
        pass

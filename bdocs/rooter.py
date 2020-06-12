import abc
from cdocs.contextual_docs import FilePath

class Rooter(metaclass=abc.ABCMeta):
    """
    Rotater creates and deletes roots
    """

    @abc.abstractmethod
    def init_root(self, rootname) -> FilePath:
        pass

    @abc.abstractmethod
    def delete_root(self) -> None:
        pass





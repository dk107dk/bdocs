import abc
from cdocs.contextual_docs import FilePath

class Rotater(metaclass=abc.ABCMeta):
    """
    Rotater moves files into backup
    """

    @abc.abstractmethod
    def rotate(self, filepath:FilePath) -> FilePath:
        pass






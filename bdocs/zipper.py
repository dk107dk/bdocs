import abc
from cdocs.contextual_docs import FilePath

class Zipper(metaclass=abc.ABCMeta):
    """
    Zipper reads and writes archives of/from doc roots
    """

    @abc.abstractmethod
    def zip(self, filepath:FilePath) -> FilePath:
        pass



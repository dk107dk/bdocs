import abc
from cdocs.contextual_docs import DocPath

class MoveDocException(Exception):
    pass

class CopyDocException(Exception):
    pass

class Mover(metaclass=abc.ABCMeta):
    """
    Movers moves docpath from place to place or makes a copy
    """

    @abc.abstractmethod
    def move_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        pass

    @abc.abstractmethod
    def copy_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        pass


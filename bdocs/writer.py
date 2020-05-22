import abc
from cdocs.contextual_docs import Doc, FilePath
from typing import Union


class Writer(metaclass=abc.ABCMeta):
    """
    Writer knows how to write bytes to a store. by default it
    writes to the filesystem.
    """

    @abc.abstractmethod
    def write(self, filepath:FilePath, content:Union[bytes, Doc]) -> None:
        pass



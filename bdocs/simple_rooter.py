import abc
from cdocs.contextual_docs import FilePath
from cdocs.config import Config
from bdocs.rooter import Rooter
import logging

class SimpleRooter(Rooter):

    def __init__(self, bdocs):
        self._bdocs = bdocs

    def init_root(self) -> None:
        logger.warning("SimpleRooter.init_root: I don't do anything yet")
        pass

    def delete_root(self) -> None:
        pass


import abc
from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.rooter import Rooter
import logging

class SimpleRooter(Rooter):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def init_root(self) -> None:
        logger.warning("SimpleRooter.init_root: I don't do anything yet")
        pass

    def delete_root(self) -> None:
        pass


import os
import shutil
from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.deleter import Deleter
import logging

class SimpleDeleter(Deleter):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def delete(self, filepath:FilePath) -> None:
        try:
            if self.isdir(filepath):
                shutil.rmtree(filepath)
            else:
                os.remove(filepath)
        except FileNotFoundError as e:
            logging.error(f'SimpleDeleter.delete: cannot delete: {e}')
            return None

    def delete_doc_tree(self, filepath:FilePath) -> None:
        self.delete(filepath)

    def isdir(self, filepath:FilePath) -> bool:
        return os.path.isdir(filepath)



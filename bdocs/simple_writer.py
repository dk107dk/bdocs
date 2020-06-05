import os.path
from cdocs.contextual_docs import Doc, FilePath
from bdocs.writer import Writer
from bdocs.building_metadata import BuildingMetadata
import logging
from typing import Union

class SimpleWriter(Writer):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def write(self, filepath:FilePath, content:Union[bytes, Doc]) -> None:
        try:
            with open(filepath, 'wb') as f:
                f.write(content)
        except FileNotFoundError as e:
            logging.error(f'SimpleWriter.write: cannot write: {e}')
            return None





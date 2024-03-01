import os.path
from cdocs.contextual_docs import Doc, FilePath
from bdocs.writer import Writer
from bdocs.building_metadata import BuildingMetadata
from cdocs.cdocs import BadDocPath
import logging
from typing import Union
from pathlib import Path

class SimpleWriter(Writer):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def write(self, filepath:FilePath, content:Union[bytes, Doc]) -> None:
        if filepath is None:
            raise BadDocPath("filepath cannot be None")
        if filepath.strip() == "":
            raise BadDocPath("filepath cannot be empty") # TODO: change to BadFilePath after next cdocs release
        try:
            head,tail = os.path.split(filepath)
            if not os.path.exists(head):
                Path(head).mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)
        except FileNotFoundError as e:
            logging.error(f'SimpleWriter.write: cannot write: {e}')
            raise BadDocPath(f"cannot write content to {filepath}")
        except Exception as e:
            logging.error(f"caught {e}")
            raise e




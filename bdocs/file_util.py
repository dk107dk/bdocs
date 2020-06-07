import os
import logging
import traceback
import shutil
from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from typing import List, Optional

class FileUtil(object):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        self._metadata = metadata
        self._bdocs = bdocs

    def get_file_names(self, path:FilePath, paths:Optional[List[str]]=[]) -> List[FilePath]:
        logging.info(f"get_file_names:   .. path: {path}, paths: {paths}")
        if not os.path.exists(path):
            logging.info(f"get_file_names:    .. doesn't exist: {path}")
        if self.isdir(path):
            for name in os.listdir(path):
                newpath = os.path.join(path, name)
                logging.info(f"get_file_names:    .. name: {name}, newpath: {newpath}")
                ss = self.get_file_names( newpath, paths )
                logging.info(f"get_file_names:    .. some: {ss} of len: {len(ss)} - {range(len(ss))}")
            logging.info(f"get_file_names:    .. done with {name}, paths: {paths}")
        else:
            logging.info(f"get_file_names:    .. append file: {path}")
            paths.append(path)
        logging.info(f"get_file_names: returning from {path}")
        return paths

    def get_dir_names(self, path:FilePath, paths:Optional[List[str]]=[]) -> List[FilePath]:
        logging.info(f"get_dir_names:   .. path: {path}, paths: {paths}")
        if not os.path.exists(path):
            logging.info(f"get_dir_names:    .. doesn't exist: {path}")
        if self.isdir(path):
            for name in os.listdir(path):
                newpath = os.path.join(path, name)
                logging.info(f"get_dir_names:    .. name: {name}, newpath: {newpath}")
                ss = self.get_file_names( newpath, paths )
                logging.info(f"get_dir_names:    .. some: {ss} of len: {len(ss)} - {range(len(ss))}")
            logging.info(f"get_dir_names:    .. done with {name}, paths: {paths}")
            paths.append(path)
        logging.info(f"get_dir_names: returning from {path}")
        return paths

    def isdir(self, filepath:FilePath) -> bool:
        return os.path.isdir(filepath)



import abc
from cdocs.contextual_docs import DocPath, FilePath
from bdocs.bdocs_config import BdocsConfig
from bdocs.mover import Mover, MoveDocException
from cdocs.simple_pather import SimplePather
import logging
import os
import shutil

class SimpleMover(Mover):

    def __init__(self, cfg:BdocsConfig, root_path:FilePath):
        self._config = cfg
        self._root_path = root_path
        self._pather = SimplePather(root_path, cfg.get_config_path()) if cfg.pather is None else cfg.pather


    def move_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        logging.debug(f"SimpleMover.move_doc: {fromdoc} -> {todoc}")
        frompath = self._pather.get_full_file_path(fromdoc)
        if not os.path.exists(frompath):
            MoveDocException(f"SimpleMover.move_doc: doc to move from {frompath} must exist")
        logging.debug(f"SimpleMover.move_doc: {fromdoc} = {frompath}")
        topath = self._pather.get_full_file_path(todoc)
        logging.debug(f"SimpleMover.move_doc: {todoc} = {topath}")
        dirindex = topath.rindex("/")
        todirpath = topath[0:dirindex]
        if not os.path.exists(todirpath):
            MoveDocException(f"SimpleMover.move_doc: dir at {todirpath} must exist")
        if not os.path.isdir(todirpath):
            MoveDocException(f"SimpleMover.move_doc: path {todirpath} must point to a directory")
        if os.path.exists(topath):
            MoveDocException(f"SimpleMover.move_doc: doc to move from {topath} must not exist")
        os.rename(frompath, topath)

    def copy_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        logging.debug(f"SimpleMover.copy_doc: {fromdoc} -> {todoc}")
        frompath = self._pather.get_full_file_path(fromdoc)
        if not os.path.exists(frompath):
            CopyDocException(f"SimpleMover.copy_doc: doc to copy from {frompath} must exist")
        logging.debug(f"SimpleMover.copy_doc: {fromdoc} = {frompath}")
        topath = self._pather.get_full_file_path(todoc)
        logging.debug(f"SimpleMover.move_doc: {todoc} = {topath}")
        dirindex = topath.rindex("/")
        todirpath = topath[0:dirindex]
        if not os.path.exists(todirpath):
            MoveDocException(f"SimpleMover.copy_doc: dir at {todirpath} must exist")
        if not os.path.isdir(todirpath):
            MoveDocException(f"SimpleMover.copy_doc: path {todirpath} must point to a directory")
        if os.path.exists(topath):
            MoveDocException(f"SimpleMover.copy_doc: doc to move from {topath} must not exist")
        shutil.copyfile(frompath, topath)


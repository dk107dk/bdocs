import os
import logging
import traceback
import shutil
from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.deleter import Deleter
from bdocs.file_util import FileUtil
from bdocs.git.git_util import GitUtil
from dulwich.repo import Repo
from dulwich import porcelain
from typing import List, Optional

class GitDeleter(Deleter):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        self._metadata = metadata
        self._bdocs = bdocs

    def delete(self, filepath:FilePath) -> None:
        util = GitUtil(self._metadata, self._bdocs)
        path = util.repo_path_for_file(filepath)
        logging.info(f"GitDeleter.delete: docroot: {self._bdocs.get_doc_root()}")
        logging.info(f"GitDeleter.delete: filepath: {filepath} ")
        logging.info(f"GitDeleter.delete: path to delete: {path}")
        try:
            docroot = self._bdocs.get_doc_root()
            #
            # setting the prefix is whacky. not sure why it is needed.
            # this does: "docs/git/" + path. which works for porcelain.rm.
            #
            p, prefix = os.path.split(docroot)
            p, pp = os.path.split(p)
            prefix = pp + os.path.sep + prefix
            porcelain.rm( self._bdocs.get_doc_root(), [ prefix + os.path.sep + path] )
            with ( util.open(self._bdocs.docs_root) ) as repo:
                commit_id = repo.do_commit(b"GitDeleter autocommit")
        except FileNotFoundError as e:
            logging.error(f'GitDeleter.delete: cannot delete: {e}')
            return None

    def delete_doc_tree(self, filepath:FilePath) -> None:
        if not self.isdir(filepath):
            logging.error(f"GitDeleter.delete_doc_tree: must be a directory: {filepath}")
        util = FileUtil(self._metadata, self._bdocs)
        paths = util.get_file_names(filepath, [])
        for path in paths:
            self.delete(path)
        shutil.rmtree(filepath)

    def isdir(self, filepath:FilePath) -> bool:
        return os.path.isdir(filepath)



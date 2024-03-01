import os.path
from cdocs.contextual_docs import Doc, FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.simple_writer import SimpleWriter
from bdocs.writer import Writer
from bdocs.git.git_util import GitUtil
import logging
from typing import Union
import traceback

class GitWriter(Writer):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        self._metadata = metadata
        self._bdocs = bdocs
        self._writer = SimpleWriter(metadata,bdocs)

    def write(self, filepath:FilePath, content:Union[bytes, Doc]) -> None:
        # write file to disk
        self._writer.write(filepath, content)
        self.stage_and_commit(filepath)

    def stage_and_commit(self, filepath:FilePath ) -> None:
        # stage and commit to git
        util = GitUtil(self._metadata, self._bdocs)
        with ( util.open(self._bdocs.docs_root) ) as repo:
            repopath = filepath[len(self._bdocs.docs_root)+1:]
            logging.info(f"GitWriter.write: repopath: {repopath}")
            try:
                repo.stage([repopath])
                commit_id = repo.do_commit(b"GitWriter autocommit")  #, committer=b"test")
                logging.info(f"GitWriter: after commit: commit_id: {commit_id}")
            except Exception as e:
                logging.error(f'GitWriter.write: cannot stage and/or commit: {e}, {type(e)}')
                traceback.print_exc()
                return None





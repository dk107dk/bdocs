import os.path
from cdocs.contextual_docs import Doc, FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.simple_writer import SimpleWriter
from bdocs.simple_user import SimpleUser
from bdocs.writer import Writer
from dulwich.repo import Repo
import logging
from typing import Union

class GitWriter(Writer):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        self._metadata = metadata
        self._bdocs = bdocs
        self._writer = SimpleWriter(metadata,bdocs)

    def write(self, filepath:FilePath, content:Union[bytes, Doc]) -> None:
        self._writer.write(filepath, content)
        try:
            repo = Repo.init(self._bdocs.docs_root)
            repopath = filepath[len(self._bdocs.docs_root)+1:]
            logging.warning(f"GitWriter.write: repopath: {repopath}")
            print(f"gitwriter: before stage")
            repo.stage([repopath])
            print(f"gitwriter: after stage")
            user = self._metadata.user
            if user is None:
                user = SimpleUser("anonymous")
            print(f"gitwriter: doing user commit")
            commit_id = repo.do_commit(b"gitwriter autocommit")  #, committer=b"test")
            print(f"gitwriter: after commit")

        except Exception as e:
            logging.error(f'GitWriter.write: cannot stage and/or commit: {e}, {type(e)}')
            return None





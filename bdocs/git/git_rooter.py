from bdocs.building_metadata import BuildingMetadata
from bdocs.rooter import Rooter
from dulwich.repo import Repo
import logging
import shutil

class GitRooter(Rooter):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._bdocs = bdocs

    def init_root(self) -> None:
        logging.info(f"GitRooter.init_root: {self._bdocs.docs_root}")
        repo = Repo.init(self._bdocs.docs_root)

    def delete_root(self) -> None:
        logging.info(f"GitRooter.delete_root: {self._bdocs.docs_root}")
        shutil.rmtree(self._bdocs.docs_root)


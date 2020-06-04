import abc
from cdocs.contextual_docs import FilePath
from cdocs.config import Config
from bdocs.rooter import Rooter
from dulwich.repo import Repo
import logging
import shutil

class GitRooter(Rooter):

    def __init__(self, bdocs):
        self._bdocs = bdocs

    def init_root(self) -> None:
        logging.warning("GitRooter.init_root: I don't do anything yet")
        repo = Repo.init(self._bdocs.docs_root)

    def delete_root(self) -> None:
        shutil.rmtree(self._bdocs.docs_root)


from bdocs.building_metadata import BuildingMetadata
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.walk import WalkEntry
import logging
import io
from typing import Optional, List
from contextlib import (
    closing,
    contextmanager,
)

class GitUtil:

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def get_log(self, paths:Optional[List[str]]=None) -> str:
        output = io.StringIO()
        if paths is not None:
            porcelain.log(paths=paths, repo=self._bdocs.get_doc_root(), outstream=output)
        else:
            porcelain.log(repo=self._bdocs.get_doc_root(), outstream=output)
        contents = output.getvalue()
        print(f"GitUil.get_log: contents {contents}")
        return contents


    #@contextmanager
    def ctxmgr(self, repopath):
        print(f"ctxmgr: path: {repopath}")
        return closing(Repo(repopath))

    def get_log_entries(self, max_entries=None, paths:Optional[List[str]]=None ) -> List[WalkEntry]:
        path = self._bdocs.get_doc_root()
        with self.ctxmgr(path) as r:
            walker = r.get_walker(max_entries=max_entries, paths=paths, reverse=False)
            for entry in walker:
                print(f">>>>> entry: {entry}")
#                def decode(x):
#                    return commit_decode(entry.commit, x)
#                print_commit(entry.commit, decode, outstream)
#                if name_status:
#                   outstream.writelines( [line+'\n' for line in print_name_status(entry.changes())])



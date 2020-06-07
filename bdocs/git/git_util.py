from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.walk import WalkEntry
from dulwich.objects import Blob
import logging
import io
from typing import Optional, List, Dict, Tuple
from contextlib import (
    closing,
    contextmanager,
)
import posixpath
import stat

class GitUtil:

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def open(self, repopath) -> Repo:
        logging.info(f"GitUtil.ctxmgr: path: {repopath}")
        return closing(Repo(repopath))

    def repo_path_for_file(self, filepath:FilePath) -> str:
        repopath = filepath[len(self._bdocs.docs_root)+1:]
        return repopath

    def get_log(self, paths:Optional[List[str]]=None) -> str:
        output = io.StringIO()
        if paths is not None:
            porcelain.log(paths=paths, repo=self._bdocs.get_doc_root(), outstream=output)
        else:
            porcelain.log(repo=self._bdocs.get_doc_root(), outstream=output)
        contents = output.getvalue()
        logging.info(f"GitUil.get_log: contents {contents}")
        return contents

    def get_log_entries(self, max_entries=None, paths:Optional[List[str]]=None ) -> List[WalkEntry]:
        path = self._bdocs.get_doc_root()
        entries = []
        with self.open(path) as r:
            walker = r.get_walker(max_entries=max_entries, paths=paths, reverse=False)
            for entry in walker:
                entries.append(entry)
            return entries

    def list_tree(self, store, treeid, base) -> Dict[str,Tuple]:
        entries = {}
        for (name, mode, sha) in store[treeid].iteritems():
            the_name = name
            if base:
                name = posixpath.join(base, name)
            entries[name] = (the_name, mode, sha)
            if stat.S_ISDIR(mode):
                entries = {**entries, **self.list_tree(store, sha, name)}
        return entries

    def get_content(self, entry:WalkEntry, path:List[str]=None) -> Dict[str,bytes]:
        with self.open(self._bdocs.get_doc_root()) as repo:
            object_store = repo.object_store
            content = {}
            for change in entry.changes():
                if path is None or change.new.path in path:
                    o = object_store[change.new.sha]
                    if isinstance( o, Blob ):
                        content[change.new.path.decode("utf-8")] = o.data
                    else:
                        logging.warning("{change.new.path} is not a blob. this may be a problem.")
            return content



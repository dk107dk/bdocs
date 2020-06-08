from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.user import User
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.walk import WalkEntry
from dulwich.objects import Blob, Commit
import logging
import io
from typing import Optional, List, Dict, Tuple
from contextlib import (
    closing,
    contextmanager,
)
import posixpath
import stat


class GitError(Exception):
    pass

class GitUtil:
    BLOG_MODE = 33188 # not sure exactly what this is yet, but it is returned by get_changes
                      # it is not the object type

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

    def tag(self, tag_name:bytes, message:bytes, user:Optional[User]=None) -> None:
        if tag_name is None:
            raise GitError("tag_name cannot be None")
        if message is None:
            raise GitError("message cannot be None")
        with self.open(self._bdocs.get_doc_root()) as repo:
            author = user.username if user is not None else None
            porcelain.tag_create(repo, tag_name, author=author, message=message, annotated=True)

    def get_tags(self) -> Dict[bytes,bytes]:
        with self.open(self._bdocs.get_doc_root()) as repo:
            tags = repo.refs.as_dict(b"refs/tags")
            for k,v in tags.items():
                tag = repo[v]
                logging.info(f"GitUtil: get_tags: {k}->tag[{v}]: {tag}")
            return tags

    def disconnect_to_tag(self, tag_name:bytes) -> None:
        with self.open(self._bdocs.get_doc_root()) as repo:
            the_name = b"refs/tags/" + tag_name
            tag = repo[the_name]
            logging.info(f"util: ... type(tag): {type(tag)}")
            ptr = tag._get_object()
            logging.info(f"util: ... type(ptr): {type(ptr)}: {len(ptr)}: {ptr}")
            commitsha = ptr[1]
            logging.info(f"util: ... type(commitsha): {type(commitsha)}: {commitsha}")
            object_store = repo.object_store
            commit = object_store.__getitem__(commitsha)
            logging.info(f"util: ... type(commit2): {type(commit)}: {commit}")
            treesha = commit._tree
            logging.info(f"util: ... type(treesha): {type(treesha)}: {treesha}")
            repo.reset_index(treesha)

    def get_changes(self, the_tag:bytes, other_tag:bytes) -> Tuple[Tuple]:
        """ returns (path, mode, objectsha) """
        logging.info(f"GitUtil.changes: the tag: {the_tag}, other tag: {other_tag}")
        with self.open(self._bdocs.get_doc_root()) as repo:
            object_store = repo.object_store
            the_name = b"refs/tags/" + the_tag
            the_tag = repo[the_name]
            logging.info(f"GitUtil.changes: the tag: {the_tag}")
            the_ptr = the_tag._get_object()
            the_commitsha = the_ptr[1]
            the_commit = object_store.__getitem__(the_commitsha)
            logging.info(f"GitUtil.changes: the commit: {the_commit}")
            the_treesha = the_commit._tree
            logging.info(f"GitUtil.changes: the treesha: {the_treesha}")

            other_name = b"refs/tags/" + other_tag
            other_tag = repo[other_name]
            logging.info(f"GitUtil.changes: other tag: {other_tag}")
            other_ptr = other_tag._get_object()
            other_commitsha = other_ptr[1]
            other_commit = object_store.__getitem__(other_commitsha)
            logging.info(f"GitUtil.changes: other commit: {other_commit}")
            other_treesha = other_commit._tree
            logging.info(f"GitUtil.changes: other treesha: {other_treesha}")

            results = []
            changes = object_store.tree_changes(the_treesha, other_treesha)
            logging.info(f"GitUtil.changes: changes: {changes}")
            for change in changes:
                logging.info(f"GitUtil.changes: a change: {change}")
                results.append(change)
            return results

    def get_content_for_change(self, change):
        with self.open(self._bdocs.get_doc_root()) as repo:
            object_store = repo.object_store
            content = {}
            i = 0
            for sha in change[2]:
                if sha is not None:
                    logging.info(f"GitUtil.get_content_for_change: the sha is: {sha}")
                    o = object_store[sha]
                    if isinstance( o, Blob ):
                        logging.info(f"GitUtil.get_content_for_change: this is a blob!: {type(o)}")
                        content[f"{i}:{change[0][i].decode('utf-8')}"] = o.data
                        logging.info(f"GitUtil.get_content_for_change: content: {content}")
                    else:
                        logging.info(f"GitUtil.get_content_for_change: not a blob!: {type(o)}")
                        content[f"{i}:{change[0][i].decode('utf-8')}"] = None
                        logging.warning("change[2].{sha} is not a blob. this may be a problem.")
                        logging.info(f"GitUtil.get_content_for_change: content: {content}")
                i = i+1
            return content


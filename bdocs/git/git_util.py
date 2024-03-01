from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.user import NamedUser
from dulwich import porcelain
from dulwich.repo import Repo
from dulwich.walk import WalkEntry
from dulwich.objects import Blob, Commit
import logging
import io
import os
from typing import Optional, List, Dict, Tuple, Any
from contextlib import (
    closing,
    contextmanager,
)
import posixpath
import stat
from datetime import datetime

class ContentChange:

    def __init__(self, tofile:bytes, tocontent:bytes ) -> None:
        self._to_file = tofile
        self._to_content = tocontent
        self._from_file = None
        self._from_content = None

    def __str__(self):
        return f"to: {self._to_file}, \n"+\
               f"to bytes: {self._to_content}, \n"+\
               f"from: {self._from_file}, \n"+\
               f"from bytes: {self._from_content}"

    @property
    def to_file(self):
        return self._to_file

    @to_file.setter
    def to_file(self, name):
        self._to_file = name

    @property
    def from_file(self):
        return self._from_file

    @from_file.setter
    def from_file(self, name):
        self._from_file = name

    @property
    def to_file_str(self):
        if self._to_file is None: return None
        return self._to_file.decode('utf-8')

    @property
    def from_file_str(self):
        if self._from_file is None: return None
        return self._from_file.decode('utf-8')

    @property
    def to_content(self):
        return self._to_content

    @to_content.setter
    def to_content(self, stuff):
        self._to_content = stuff

    @property
    def from_content(self):
        return self._from_content

    @from_content.setter
    def from_content(self, stuff):
        self._from_content = stuff


class GitError(Exception):
    pass

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

    def tag(self, tag_name:bytes, message:bytes, user:Optional[NamedUser]=None) -> None:
        if tag_name is None:
            raise GitError("tag_name cannot be None")
        if message is None:
            raise GitError("message cannot be None")
        with self.open(self._bdocs.get_doc_root()) as repo:
            author = user.name_of_user if user is not None else None
            porcelain.tag_create(repo, tag_name, author=author, message=message, annotated=True)

    def get_tags(self) -> Dict[bytes,bytes]:
        with self.open(self._bdocs.get_doc_root()) as repo:
            tags = repo.refs.as_dict(b"refs/tags")
            for k,v in tags.items():
                tag = repo[v]
                print(f"GitUtil.get_tags: {k}->tag[{v}]: {tag}")
                print(f"GitUtil.get_tags: {tag._tag_time}")
                print(f"GitUtil.get_tags: {tag._tagger}")
                print(f"GitUtil.get_tags: {tag._message}")
            return tags

    def get_tag_values(self) -> Dict[str,Dict[str,Any]]:
        """ gets a dict of
                {
                    sha: dict{
                          "name",
                          "tagger",
                          "message",
                          "timestamp",
                          "datetime",
                          "object"
                    }
                }
        """
        with self.open(self._bdocs.get_doc_root()) as repo:
            tags = repo.refs.as_dict(b"refs/tags")
            result = {}
            for k,v in tags.items():
                tag = repo[v]
                print(f"GitUtil.get_tags: {k}->tag[{v}]: {tag}")
                atag = {}
                result[v.decode("utf-8")] = atag
                atag["name"] = tag._name
                atag["tagger"] = tag._tagger
                atag["message"] = tag._message
                atag["timestamp"] = tag._tag_time
                dt = datetime.fromtimestamp(tag._tag_time)
                atag["datetime"] = dt
                atag["object"] = tag
            return result

    # is disconnect_to_tag the right name? it basically sets head to point to tag.
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

    def get_content_for_change(self, change) -> Dict[bytes,ContentChange]:
        with self.open(self._bdocs.get_doc_root()) as repo:
            object_store = repo.object_store
            content = {}
            i = 0
            for sha in change[2]:
                if sha is not None:
                    logging.info(f"GitUtil.get_content_for_change: the sha is: {sha}")
                    o = object_store[sha]
                    file = change[0][i]
                    c = content.get(file)
                    if c is None:
                        c = ContentChange(file, o.data if isinstance( o, Blob ) else None)
                        content[file] = c
                    else:
                        c.from_file = file
                        c.from_content = o.data if isinstance( o, Blob ) else None

                    if isinstance( o, Blob ):
                        logging.info(f"GitUtil.get_content_for_change: this is a blob!: {type(o)}")
                    else:
                        logging.info(f"GitUtil.get_content_for_change: not a blob!: {type(o)}")
                    logging.info(f"GitUtil.get_content_for_change: content: {content}")
                i = i+1
            return content

    def sync_file_system(self, c:ContentChange, revert:bool=True ) -> None:
        logging.info(f"GitUtil.sync_file_system: syncing: {c}")

        writing = (not revert and c.to_content is not None) or \
                  (revert and c.from_content is not None)
        write = None
        write_to = None
        if writing:
            if revert:
                write = c.from_content
                write_to = c.from_file_str
            else:
                write = c.to_content
                write_to = c.to_file_str
        deleting = not write
        delete = None
        if deleting:
            if revert:
                delete = c.to_file_str
            else:
                delete = c.from_file_str

        logging.info(f"GitUtil.sync_file_system: writing? to_file: {c.to_file}, revert: {revert}, from_file: {c.from_file}, writing: {writing}")
        if writing:
            path = os.path.join(self._bdocs.get_doc_root(), write_to )
            logging.info(f"GitUtil.sync_file_system: write path: {path}")
            with open( path, 'wb') as file:
                file.write(write)
        else:
            path = os.path.join(self._bdocs.get_doc_root(), delete)
            try:
                logging.info(f"GitUtil.sync_file_system: delete path: {path}")
                os.remove(path)
            except FileNotFoundError as e:
                logging.error(f'GitUtil.sync_file_system: cannot delete {c.from_file_str}: {e}')



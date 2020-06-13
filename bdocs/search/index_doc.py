from cdocs.contextual_docs import JsonDict
from typing import Optional
import inspect

class IndexDoc(object):

    def __init__(self, doc:Optional[JsonDict]=None) -> None:
        self._root=None
        self._path=None
        self._paths=None
        self._author=None
        self._contributors=None
        self._content=None
        self._title=None
        self._created=None
        self._updated=None
        if doc is not None:
            self._from_json(doc)

    def _from_json(self, doc) -> None:
        for k,v in doc.items():
            setattr(self, "_"+k, v)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, val):
        self._root = val

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        self._path = val

    @property
    def paths(self):
        return self._paths

    @paths.setter
    def paths(self, val):
        self._paths = val

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, val):
        self._author = val

    @property
    def contributors(self):
        return self._contributors

    @contributors.setter
    def contributors(self, val):
        self._contributors = val

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, val):
        self._content = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        self._title = val

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, val):
        self._created = val

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, val):
        self._updated = val



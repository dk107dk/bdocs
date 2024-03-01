from typing import Optional, Dict, List
from cdocs.contextual_docs import FilePath, JsonDict
import logging

class RootInfo(object):
    """
    accepts: the types of requests accepted: cdocs, binary, html, etc.
    formats: the types of files (by extension) that are looked for and used
    notfound: a notfound docpath to return if the requested docpath is not there
    features: a list of features supported on the root
    search: does the root have a search index?
    transform: does the root do transformations before returning content?
    git: does the root use git?
    public: is the root available to the public without API key?
    """
    def __init__(self):
        self._accepts:List[str] = None
        self._name:str = None
        self._file_path:FilePath = None
        self._formats:List[str] = None
        self._features:List[str] = None
        self._notfound:str = None
        self._git:bool = None
        self._search:bool = None
        self._transform:bool = None
        self._edit_cdocs_json:bool = None
        self._public:bool = None
        self._rules:bool = None

    def __str__(self):
        return f"{type(self)}: name: {self.name}, path: {self.file_path},\
 accepts: {self.accepts}, formats: {self.formats}, features: {self.features},\
 notfound: {self.notfound}"

    def to_json(self) -> JsonDict:
        print(f"RootInfo.to_json")
        d = { "name":self.name,
                 "file_path": self.file_path,
                 "accepts": self.accepts,
                 "formats": self.formats,
                 "notfound": self.notfound,
                 "features": self.features,
                 "search": self.search,
                 "git": self.git,
                 "transform": self.transform,
                 "edit_cdocs_json": self.edit_cdocs_json,
                 "public": self.public
               }
        # make sure all features are present in json
        for f in self.features:
            print(f"RootInfo.to_json: adding f: {f}")
            d[f] = True
        return d

    @property
    def accepts(self):
        return self._accepts

    @accepts.setter
    def accepts(self, val):
        self._accepts = val

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, val):
        self._file_path = val

    @property
    def formats(self):
        return self._formats

    @formats.setter
    def formats(self, val):
        self._formats = val

    @property
    def notfound(self):
        return self._notfound

    @notfound.setter
    def notfound(self, val):
        self._notfound = val

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, val):
        self._features = val

    @property
    def search(self):
        if self._search is None:
            self._search = "search" in self.features
        return self._search

    @search.setter
    def search(self, val):
        self._search = val

    @property
    def git(self):
        if self._git is None:
            self._git = "git" in self.features
        return self._git

    @git.setter
    def git(self, val):
        self._git = val

    @property
    def transform(self):
        if self._transform is None:
            self._transform = "transform" in self.features
        return self._transform

    @transform.setter
    def transform(self, val):
        self._transform = val

    @property
    def edit_cdocs_json(self):
        if self._edit_cdocs_json is None:
            self._edit_cdocs_json = "edit_cdocs_json" in self.features
        return self._edit_cdocs_json

    @edit_cdocs_json.setter
    def edit_cdocs_json(self, val):
        self._edit_cdocs_json = val

    @property
    def public(self):
        if self._public is None:
            self._public = "public" in self.features
        return self._public

    @public.setter
    def public(self, val):
        self._public = val

    @property
    def rules(self):
        if self._rules is None:
            self._rules = "rules" in self.features
        return self._rules

    @rules.setter
    def rules(self, val):
        self._rules = val





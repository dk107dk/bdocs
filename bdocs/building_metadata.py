import abc
from typing import Union, Optional, Dict,List
from bdocs.search_options import SearchOptions
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.context_metadata import ContextMetadata
from bdocs.bdocs_config import BdocsConfig
from cdocs.config import Config
from bdocs.user import User
import logging

class RootInfo(object):
    """
    accepts: the types of requests accepted: cdocs, binary, html, etc.
    formats: the types of files (by extension) that are looked for and used
    notfound: a notfound docpath to return if the requested docpath is not there
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
        self._notfound:str = None
        self._git = None
        self._search = None
        self._transform = None
        self._edit_cdocs_json = None
        self._public = None

    def __str__(self):
        return f"{type(self)}: name: {self.name}, path: {self.file_path}, accepts: {self.accepts}, formats: {self.formats}, notfound: {self.notfound}"

    def to_json(self):
        return { "name":self.name,
                "file_path": self.file_path,
                 "accepts": self.accepts,
                 "formats": self.formats,
                 "notfound": self.notfound,
                 "search": self.search,
                 "git": self.git,
                 "transform": self.transform,
                 "edit_cdocs_json": self.edit_cdocs_json,
                 "public": self.public
               }

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
        return self._search

    @search.setter
    def search(self, val):
        self._search = val

    @property
    def git(self):
        return self._git

    @git.setter
    def git(self, val):
        self._git = val

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, val):
        self._transform = val

    @property
    def edit_cdocs_json(self):
        return self._edit_cdocs_json

    @edit_cdocs_json.setter
    def edit_cdocs_json(self, val):
        self._edit_cdocs_json = val

    @property
    def public(self):
        return self._public

    @public.setter
    def public(self, val):
        self._public = val




class BuildingMetadata(ContextMetadata):

    def __init__(self, config:Optional[Config]=None, user:Optional[User]=None) -> None:
        super().__init__(config)
        self._user = user
        self._features = {_[0]:[s for s in _[1].split(",")] for _ in self.config.get_items("features")}
        logging.info(f"BuildingMetadata.__init__: features: {self.features}")
        self._offers_feature = dict()
        for k in self._features:
            v = self._features[k]
            for av in v:
                fs = self._offers_feature.get(av)
                if fs is None:
                    fs = []
                fs.append(k)
                self._offers_feature[av] = fs
        for root in self.root_names:
            rfs = self.features.get(root)
            if rfs is None:
                logging.info(f"BuildingMetadata.__init__: features of {root} are None")
                dfs = self.config.get("defaults", "features")
                if dfs is not None:
                    self.features[root] = dfs.split(",")
                    for av in self.features[root]:
                        fs = self._offers_feature.get(av)
                        if fs is None:
                            fs = []
                        fs.append(k)
                        self._offers_feature[av] = fs
            else:
                logging.info(f"BuildingMetadata.__init__: not None: features of {root} are {rfs}")

    @property
    def offers_feature(self) -> Dict[str,List[str]]:
        return self._offers_feature

    @property
    def features(self) -> Dict[str,List[str]]:
        return self._features

    @property
    def user(self) -> User:
        return self._user

    def get_root_info(self, rootname:str) -> JsonDict:
        if self.keyed_roots[rootname] is None:
            logging.warn(f"BuildingMetadata.get_root_info: {rootname} is not a root")
            return None
        root_info = RootInfo()
        accepts = self.accepts[rootname]
        root_info.accepts = accepts
        root_info.formats = self.formats[rootname]
        root_info.file_path = self._keyed_roots[rootname]
        root_info.notfound = self.config.get("notfound", rootname)
        features = self.config.get("features", rootname )
        if features is None:
            root_info.search = False
            root_info.git = False
            root_info.transform = False
            root_info.edit_cdocs_json = False
        else:
            fs = features.split(",")
            if "search" in fs:
                root_info.search = True
            if "git" in fs:
                root_info.git = True
            if "edit_cdocs_json" in fs:
                root_info.edit_cdocs_json = False
            if "transform" in fs:
                root_info.transform = False
        root_info.features = features
        root_info.name = rootname
        return root_info


import abc
from typing import Union, Optional, Dict,List
from bdocs.search_options import SearchOptions
from bdocs.root_info import RootInfo
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.context_metadata import ContextMetadata
from bdocs.bdocs_config import BdocsConfig
from cdocs.config import Config
import logging


class BuildingMetadata(ContextMetadata):

    def __init__(self, config:Optional[Config]=None) -> None:
        super().__init__(config)
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
            root_info.public = True
            root_info.rules = False
        else:
            fs = self.features[rootname] #features.split(",")
            if "search" in fs:
                root_info.search = True
            if "git" in fs:
                root_info.git = True
            if "edit_cdocs_json" in fs:
                root_info.edit_cdocs_json = True
            if "transform" in fs:
                root_info.transform = True
        root_info.features = self.features[rootname]
        root_info.name = rootname
        return root_info


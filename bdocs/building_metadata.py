import abc
from typing import Union, Optional, Dict
from bdocs.search_options import SearchOptions
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.context_metadata import ContextMetadata
from bdocs.bdocs_config import BdocsConfig
from cdocs.config import Config
from bdocs.user import User


class BuildingMetadata(ContextMetadata):

    def __init(self, config:Optional[Config]=None, user:Optional[User]=None) -> None:
        super(config)
        self._user = user

    @property
    def user(self) -> User:
        return self._user



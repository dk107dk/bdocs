import os
import logging
from typing import Optional
from bdocs.bdocs_config import BdocsConfig

APP_CONFIG_PATH = "config/app-config.ini"

class AppConfig(BdocsConfig):

    def __init__(self, path:Optional[str]=None):
        if path is None:
            self._path = APP_CONFIG_PATH
            logging.debug(f"AppConfig.__init__ without config path. using : {os.getcwd()}/{APP_CONFIG_PATH}")
        super().__init__(self._path)





import os
from application.app_config import AppConfig
from cdocs.contextual_docs import FilePath

CONFIG_FILE_NAME = "config.ini"
CONFIG_DIR = "config"
DOCS_DIR_NAME = "docs"
TEMP_DIR_NAME = "tmp"


class PathsFinder(object):

    def __init__(self):
        self._config = AppConfig()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, cfg):
        self._config = cfg

# ============


    def get_project_config_dir_path(self, accountid:str, teamid:str, projectid:str) -> FilePath:
        path = self.get_project_path(accountid, teamid, projectid) + os.sep + CONFIG_DIR
        if os.path.exists(path):
            pass
        else:
            self.mkdir(path)
        return path

    def get_project_config_file_path(self, accountid:str, teamid:str, projectid:str) -> FilePath:
        path = self.get_project_config_dir_path(accountid, teamid, projectid) + os.sep + CONFIG_FILE_NAME
        return path

    def get_ur_root_path(self) -> FilePath:
        cfg = self.config
        ur_root = cfg.get("ur", "root")
        return ur_root

    def get_home_path(self, accountid:str) -> FilePath:
        """
        gets the home dir for an account. team dirs are created here.
        """
        cfg = self.config
        ur_root = cfg.get("ur", "root")
        print(f"DocRootManagement.get_home_path_of: ur_root: {ur_root}, accountid: {accountid}")
        home = ur_root + os.sep + accountid[0:1]
        print(f"DocRootManagement.get_home_path_of: home 1: {home}")
        home = home + os.sep + accountid[1:2]
        print(f"DocRootManagement.get_home_path_of: home 2: {home}")
        home = home + os.sep + accountid
        print(f"DocRootManagement.get_home_path_of: home 4: {home}")
        self.mkdir(home)
        return home

    def get_team_path(self, accountid:str, teamid:str) -> FilePath:
        path = self.get_home_path(accountid)
        path += os.sep + teamid
        self.mkdir(path)
        return path

    def get_project_path( self, accountid:str, teamid:str, projectid:str ) -> FilePath:
        path = self.get_team_path(accountid, teamid)
        path += os.sep + projectid
        self.mkdir(path)
        return path

    def get_project_temp_dir_path( self, accountid:str, teamid:str, projectid:str ) -> FilePath:
        path = self.get_project_path(accountid, teamid, projectid)
        path += os.sep + TEMP_DIR_NAME
        self.mkdir(path)
        return path

    def get_project_docs_dir_path( self, accountid:str, teamid:str, projectid:str ) -> FilePath:
        path = self.get_project_path(accountid, teamid, projectid)
        path += os.sep + DOCS_DIR_NAME
        self.mkdir(path)
        return path

    def mkdir(self, path) -> None:
        try:
            print(f"PathFinder.mkdir: making directory: {path}")
            os.makedirs(path)
        except Exception as e:
            print(f"error!: {e}")




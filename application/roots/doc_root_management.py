import os
from application.app_config import AppConfig
from application.roots.paths_finder import PathsFinder
from bdocs.bdocs_config import BdocsConfig
from cdocs.contextual_docs import FilePath
from bdocs.root_info import RootInfo

DEFAULT_ROOT_NAME = "default"
DEFAULT_ROOT_JSON_NAME = "default_json"

class SuspiciousFilePath(Exception):
    pass

class DocRootManagement(object):

    def __init__(self):
        self._config = AppConfig()
        self._finder = PathsFinder()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, cfg):
        self._config = cfg

    @property
    def finder(self):
        return self._finder

    @finder.setter
    def finder(self, f):
        self._finder = f

# ============

    def get_config_of(self, accountid:str, teamid:str, projectid:str) -> BdocsConfig:
        path = self.generate_config_if(accountid, teamid, projectid)
        cfg = BdocsConfig( path )
        return cfg

    def get_config_of(self, accountid:str, teamid:str, projectid:str) -> BdocsConfig:
        path = self.generate_config_if(accountid, teamid, projectid)
        cfg = BdocsConfig( path )
        return cfg

    def create_standard_root(self, accountid:str, teamid:str, projectid:str, rootname:str ) -> None:
        rootinfo = RootInfo()
        path = self.finder.get_project_docs_dir_path(accountid, teamid, projectid)
        thedir = path + os.sep + rootname
        rootinfo.name = rootname
        rootinfo.file_path = thedir
        rootinfo.accepts = ["cdocs"]
        rootinfo.formats = ["xml"]
        rootinfo.features = ["search","git","transform","edit_cdocs_json"]
        rootinfo.notfound = rootname + "/404.xml"
        self.create_root(accountid, teamid, projectid, rootinfo)

    def create_root(self, accountid:str, teamid:str, projectid:str, rootinfo:RootInfo ) -> None:
        path = self.generate_config_if(accountid, teamid, projectid)
        cfg = BdocsConfig(path)
        self.add_rootinfo_to_config(cfg, rootinfo)
        self._create_default_notfound_if(accountid,teamid,projectid,rootinfo.notfound)

    def _create_default_notfound_if(self, accountid:str, teamid:str, projectid:str, rootplusdocpath):
        print(f"DocRootManagement._create_default_notfound_if: a,t,p ids {accountid}, {teamid}, {projectid}, rootplusdocpath: {rootplusdocpath}")
        if rootplusdocpath is None:
            return
        if rootplusdocpath.find("..") > -1:
            logging.error(f"DocRootManagement._create_default_notfound_if:\
 relative path in {path}: ids:\
 {accountid}, {teamid}, {projectid}")
            raise SuspiciousFilePath([accountid,teamid,projectid,path])
        path = self.generate_config_if(accountid, teamid, projectid)
        cfg = BdocsConfig(path)
        notfoundpath = cfg.get("locations", "docs_dir")
        if rootplusdocpath[0:1] == '/':
            pass
        else:
            rootplusdocpath = os.sep + rootplusdocpath
        notfoundpath += rootplusdocpath
        if os.path.exists(notfoundpath):
            pass
        else:
            nf = ''
            if notfoundpath.find(".xml") > -1:
                nf = "<not_found>Couldn't find that for you</not_found>"
            else:
                nf = "not found"
            with open(notfoundpath, 'w') as f:
                f.write(nf)

    def create_project(self, accountid:str, teamid:str, projectid:str) -> None:
        self.generate_config_if(accountid, teamid, projectid)

    def generate_config_if(self, accountid:str, teamid:str, projectid:str) -> FilePath:
        path = self.finder.get_project_config_file_path(accountid, teamid, projectid)
        if os.path.exists(path):
            pass
        else:
            self.generate_config(accountid, teamid, projectid)
        return path

    def generate_config(self, accountid:str, teamid:str, projectid:str) -> None:
        rootinfo = RootInfo()
        path = self.finder.get_project_docs_dir_path(accountid, teamid, projectid)
        thedir = path + os.sep + DEFAULT_ROOT_NAME
        rootinfo.name = DEFAULT_ROOT_NAME
        rootinfo.file_path = thedir
        rootinfo.accepts = ["cdocs"]
        rootinfo.formats = ["xml"]
        rootinfo.features = ["search","git","transform","edit_cdocs_json"]
        rootinfo.notfound = DEFAULT_ROOT_NAME + "/404.xml"
        self.generate_config_from_root_info(accountid, teamid, projectid, rootinfo)

    def generate_config_from_root_info(self, accountid:str, \
                                             teamid:str, projectid:str, \
                                             rootinfo:RootInfo ) -> None:
        ur_root = self.finder.get_ur_root_path()
        thecfg = BdocsConfig( self.finder.get_project_config_file_path(accountid, teamid, projectid) )
        path = self.finder.get_project_docs_dir_path(accountid, teamid, projectid)
        thepath = path + os.sep + rootinfo.name
        print(f"DocRootManagement.generate_config_from_root_info: mkdir on {thepath}")
        self.finder.mkdir(thepath)
        self.add_rootinfo_to_config(thecfg, rootinfo)
        thecfg.just_add_to_config("notfound", rootinfo.name, rootinfo.notfound )
        thecfg.just_add_to_config("defaults", "features", "search,git,transform" )
        thecfg.just_add_to_config("defaults", "ext", "xml" )
        thecfg.just_add_to_config("defaults", "nosplitplus", "" )
        thecfg.just_add_to_config("filenames", "tokens", "tokens.json" )
        thecfg.just_add_to_config("filenames", "labels", "labels.json" )
        thecfg.just_add_to_config("filenames", "hashmark", "*" )
        thecfg.just_add_to_config("filenames", "plus", "+" )
        thecfg.just_add_to_config("locations", "temp_dir", self.finder.get_project_temp_dir_path(accountid, teamid, projectid) )
        thecfg.just_add_to_config("locations", "docs_dir", path )
        thecfg.save_config()
        self._create_default_notfound_if(accountid,teamid,projectid,rootinfo.notfound)

    def add_rootinfo_to_config(self, thecfg:BdocsConfig, rootinfo:RootInfo ) -> None:
        thecfg.just_add_to_config("docs", rootinfo.name, rootinfo.file_path )
        if "edit_cdocs_json" in rootinfo.features:
            thecfg.just_add_to_config("docs", rootinfo.name + "_json", rootinfo.file_path + "_json" )
            thecfg.just_add_to_config("accepts", rootinfo.name + "_json", "json" )
            thecfg.just_add_to_config("features", rootinfo.name + "_json", "search" )
            thecfg.just_add_to_config("formats", rootinfo.name + "_json", "json" )
        accepts = ','.join( rootinfo.accepts )
        thecfg.just_add_to_config("accepts", rootinfo.name, accepts )
        if rootinfo.features is not None:
            features = ','.join( rootinfo.features )
            thecfg.just_add_to_config("features", rootinfo.name, features )
        formats = ','.join( rootinfo.formats )
        thecfg.just_add_to_config("formats", rootinfo.name, formats )
        thecfg.save_config()



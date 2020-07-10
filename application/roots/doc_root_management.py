import os
import logging
from typing import List
from application.app_config import AppConfig
from application.roots.paths_finder import PathsFinder
from bdocs.bdocs_config import BdocsConfig
from cdocs.contextual_docs import FilePath
from bdocs.root_info import RootInfo
import shutil
from pathlib import Path

DEFAULT_ROOT_NAME = "my_project"
DEFAULT_ROOT_JSON_NAME = DEFAULT_ROOT_NAME + "_json"
DEFAULT_TEST_FILE = DEFAULT_ROOT_NAME + "/test_doc.xml"

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

    def delete_all_projects(self):
        root = self._config.get("ur", "root")
        print(f"DocRootManagement.delete_all_projects: root: {root}")
        dirs = [os.path.join(root, o) for o in os.listdir(root) if os.path.isdir(os.path.join(root,o))]
        print(f"DocRootManagement.delete_all_projects: dirs: {dirs}")
        for d in dirs:
            print(f"DocRootManagement.delete_all_projects: deleting: {d}")
            shutil.rmtree(d)

    def delete_root(self, accountid, teamid, projectid, rootname ) -> None:
        docspath = self.finder.get_project_docs_dir_path( accountid, teamid, projectid )
        docspath += os.sep + rootname
        shutil.rmtree(docspath)

    def get_config_of(self, accountid, teamid, projectid) -> BdocsConfig:
        path = self.generate_config_if(accountid, teamid, projectid)
        cfg = BdocsConfig( path )
        return cfg

    def get_roots(self, accountid, teamid, projectid) -> List[str]:
        cfg = self.get_config_of(accountid, teamid, projectid)
        roots = cfg.get_items("docs")
        return roots

    def get_number_of_roots(self, accountid, teamid, projectid) -> int:
        roots = self.get_roots(accountid, teamid, projectid)
        return len(roots)

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
        self._create_default_test_file_if(accountid,teamid,projectid, DEFAULT_TEST_FILE )

    def _create_default_notfound_if(self, accountid:str, teamid:str, projectid:str, rootplusdocpath):
        logging.info(f"DocRootManagement._create_default_notfound_if: a,t,p ids {accountid}, {teamid}, {projectid}, rootplusdocpath: {rootplusdocpath}")
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


    def _create_default_test_file_if(self, accountid:str, teamid:str, projectid:str, rootplusdocpath):
        logging.info(f"DocRootManagement._create_test_file_if: a,t,p ids {accountid}, {teamid}, {projectid}, rootplusdocpath: {rootplusdocpath}")
        if rootplusdocpath is None:
            return
        if rootplusdocpath.find("..") > -1:
            logging.error(f"DocRootManagement._create_default_test_file_if:\
 relative path in {path}: ids:\
 {accountid}, {teamid}, {projectid}")
            raise SuspiciousFilePath([accountid,teamid,projectid,path])
        path = self.finder.get_project_config_file_path(accountid, teamid, projectid)
        cfg = BdocsConfig(path)
        docs_dir = cfg.get("locations", "docs_dir")
        if rootplusdocpath[0:1] == '/':
            pass
        else:
            rootplusdocpath = os.sep + rootplusdocpath
        test_file_path = docs_dir + rootplusdocpath
        if os.path.exists(test_file_path):
            pass
        else:
            test_file_dir = test_file_path[0:test_file_path.rindex('/')]
            print(f"DocRootManagement._create_default_test_file_if: test_file_dir: {test_file_dir}")
            Path(test_file_dir).mkdir(parents=True, exist_ok=True)
            test_file = 'Hello World!'
            if test_file_path.find(".xml") > -1:
                test_file = f"<doc>{test_file}</doc>"
            else:
                test_file = "not found"
            with open(test_file_path, 'w') as f:
                f.write(test_file)



    def create_project(self, accountid, teamid, projectid) -> None:
        self.generate_config_if(accountid, teamid, projectid)

    def generate_config_if(self, accountid, teamid, projectid) -> FilePath:
        path = self.finder.get_project_config_file_path(accountid, teamid, projectid)
        if os.path.exists(path):
            pass
        else:
            self.generate_config(accountid, teamid, projectid)
        return path

    def generate_config(self, accountid, teamid, projectid) -> None:
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

    def generate_config_from_root_info(self, accountid, \
                                             teamid, projectid, \
                                             rootinfo:RootInfo ) -> None:
        ur_root = self.finder.get_ur_root_path()
        thecfg = BdocsConfig( self.finder.get_project_config_file_path(accountid, teamid, projectid) )
        path = self.finder.get_project_docs_dir_path(accountid, teamid, projectid)
        thepath = path + os.sep + rootinfo.name
        logging.info(f"DocRootManagement.generate_config_from_root_info: mkdir on {thepath}")
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
        self._create_default_test_file_if(accountid,teamid,projectid, DEFAULT_TEST_FILE)

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



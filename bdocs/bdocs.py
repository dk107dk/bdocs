from typing import Optional, Union
from cdocs.contextual_docs import Doc, FilePath, DocPath, JsonDict
from bdocs.building_docs import BuildingDocs
from cdocs.cdocs import Cdocs, BadDocPath
from cdocs.config import Config
from bdocs.writer import Writer
from bdocs.zipper import Zipper
from bdocs.walker import Walker
from cdocs.pather import Pather
from bdocs.deleter import Deleter
from bdocs.rotater import Rotater
from bdocs.simple_rotater import SimpleRotater
from bdocs.simple_zipper import SimpleZipper
from cdocs.simple_pather import SimplePather
from bdocs.simple_writer import SimpleWriter
from bdocs.simple_walker import SimpleWalker
from bdocs.bdocs_config import BdocsConfig
from bdocs.simple_deleter import SimpleDeleter
import os
from zipfile import ZipFile
from  uuid import uuid4
import shutil

def _tempname() -> str:
    return str(uuid4()).replace('-', '_')



class Bdocs(BuildingDocs):

    def __init__(self, doc_root:FilePath, config:Optional[Config]=None):
        self._docs_root = doc_root
        cfg = BdocsConfig(None) if config is None else config
        self._config = cfg
        self._writer = SimpleWriter()
        self._walker = SimpleWalker()
        self._deleter = SimpleDeleter()
        self._zipper = SimpleZipper()
        self._rotater = SimpleRotater()
        self._pather = SimplePather(self._docs_root, cfg.get_config_path()) if cfg.pather is None else cfg.pather

    @property
    def zipper(self) -> Zipper:
        return self._zipper

    @property
    def deleter(self) -> Deleter:
        return self._deleter

    @property
    def rotater(self) -> Rotater:
        return self._rotater

    @property
    def writer(self) -> Writer:
        return self._writer

    @property
    def walker(self) -> Walker:
        return self._walker

    @property
    def pather(self) -> Pather:
        return self._pather

    @property
    def config(self) -> Config:
        return self._config


# ------------------

    def get_docs_root(self) -> FilePath:
        return self._docs_root

    def put_doc(self, path:DocPath, doc:Union[bytes,Doc]) -> None:
        filepath:FilePath = self.pather.get_full_file_path(path)
        if type(doc) == 'bytes':
            bs = doc
        else:
            bs = doc.encode()
        self.writer.write(filepath, bs)

    def delete_doc(self, path:DocPath) -> None:
        filepath:FilePath = self.pather.get_full_file_path(path)
        self.deleter.delete(filepath)

    def delete_doc_tree(self, path:DocPath) -> None:
        filepath = self.get_dir_for_docpath(path)
        self.deleter.delete(filepath)

    def get_dir_for_docpath(self, path:DocPath) -> FilePath:
        filepath:FilePath = self.pather.get_full_file_path(path)
        index = filepath.rindex(".")
        filepath = filepath[0:index]
        return filepath

    def doc_exists(self, path:DocPath) -> bool:
        filepath:FilePath = self.pather.get_full_file_path(path)
        return os.path.exists(filepath)

    def get_doc_tree(self) -> JsonDict:
        return self.walker.get_doc_tree(self)

    def zip_doc_tree(self) -> FilePath:
        return self.zipper.zip(self.get_dir_for_docpath("/"))

    # this doesn't belong here because this Bdocs has its own root and shouldn't be
    # messing around with unzipping another root
    def unzip_doc_tree(self, zipfile:FilePath) -> None:
        if not os.path.exists(zipfile):
            raise Exception(f"no file at {zipfile}")
        zipfilename = zipfile[zipfile.rindex(os.sep)+1:]
        tmpdir = self.config.get("locations", "temp_dir")
        unzipdirname = _tempname()
        tempzipdir = tmpdir + os.sep + unzipdirname
        os.mkdir(tempzipdir)
        unzipme =  tempzipdir + os.sep + zipfilename
        os.rename( zipfile, unzipme )
        with ZipFile(unzipme, 'r') as z:
            z.extractall(tempzipdir )
        # there should be a single directory -- the root -- and the zipfile
        files = os.listdir(tempzipdir)
        if len(files) != 2:
            raise Exception(f"there should be just 2 files at {tempzipdir}, but there are: {files}")
        newrootname = [_ for _ in files if _ != zipfilename ][0]
        self.add_root_dir( newrootname, tempzipdir + os.sep + newrootname)
        shutil.rmtree(tempzipdir)

    def add_root_dir(self, newrootname:str, whereitisnow:FilePath) -> None:
        docsdir = self.config.get("locations", "docs_dir")
        whereitsgoing = docsdir + os.sep + newrootname
        if os.path.exists(whereitsgoing):
            self.move_root(whereitsgoing)
        os.rename( whereitisnow, whereitsgoing )
        self.config.add_to_config("docs", newrootname, whereitsgoing)

    def move_root(self, path:FilePath) -> FilePath:
        return self.rotater.rotate(path)









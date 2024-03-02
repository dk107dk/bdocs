from  uuid import uuid4
import shutil
import os
import logging
from cdocs.contextual_docs import FilePath
from bdocs.zipper import Zipper
from bdocs.simple_rotater import SimpleRotater
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs_config import BdocsConfig
from zipfile import ZipFile

class SimpleZipper(Zipper):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def zip(self, filepath:FilePath) -> FilePath:
        auuid =  uuid4()
        auuid = str(auuid).replace('-', '_')
        result = shutil.make_archive(auuid, 'zip', filepath)
        return result

    def unzip_doc_tree(self, zipfile:FilePath) -> None:
        if not os.path.exists(zipfile):
            raise Exception(f"no file at {zipfile}")
        zipfilename = zipfile[zipfile.rindex(os.sep)+1:]
        tmpdir = self._metadata.config.get("locations", "temp_dir")
        unzipdirname = self._tempname()
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
        docsdir = self._metadata.config.get("locations", "docs_dir")
        whereitsgoing = docsdir + os.sep + newrootname
        if os.path.exists(whereitsgoing):
            self.move_root(whereitsgoing)
        os.rename( whereitisnow, whereitsgoing )
        self._metadata.config.add_to_config("docs", newrootname, whereitsgoing)

    def move_root(self, path:FilePath) -> FilePath:
        return SimpleRotater(self._metadata, self._bdocs).rotate(path)

    def _tempname(self) -> str:
        return str(uuid4()).replace('-', '_')



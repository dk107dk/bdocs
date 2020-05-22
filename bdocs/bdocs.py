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
from bdocs.simple_zipper import SimpleZipper
from cdocs.simple_pather import SimplePather
from bdocs.simple_writer import SimpleWriter
from bdocs.simple_walker import SimpleWalker
from cdocs.simple_config import SimpleConfig
from bdocs.simple_deleter import SimpleDeleter
import os

class Bdocs(BuildingDocs):

    def __init__(self, doc_root:FilePath, config:Optional[Config]=None):
        self._docs_root = doc_root
        cfg = SimpleConfig(None) if config is None else config
        self._writer = SimpleWriter()
        self._walker = SimpleWalker()
        self._deleter = SimpleDeleter()
        self._zipper = SimpleZipper()
        self._pather = SimplePather(self._docs_root, cfg.get_config_path()) if cfg.pather is None else cfg.pather

    @property
    def zipper(self) -> Zipper:
        return self._zipper

    @property
    def deleter(self) -> Deleter:
        return self._deleter

    @property
    def writer(self) -> Writer:
        return self._writer

    @property
    def walker(self) -> Walker:
        return self._walker

    @property
    def pather(self) -> Pather:
        return self._pather

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
        print(f"get_dir_for_docpath 1: {filepath}")
        index = filepath.rindex(".")
        filepath = filepath[0:index]
        print(f"get_dir_for_docpath 2: {filepath}")
        return filepath

    def doc_exists(self, path:DocPath) -> bool:
        filepath:FilePath = self.pather.get_full_file_path(path)
        return os.path.exists(filepath)

    def get_doc_tree(self) -> JsonDict:
        return self.walker.get_doc_tree(self)

    def zip_doc_tree(self) -> FilePath:
        return self.zipper.zip(self.get_dir_for_docpath("/"))


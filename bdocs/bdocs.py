import os
from  uuid import uuid4
import shutil
from typing import Optional, Union, List, Tuple, Dict
from cdocs.contextual_docs import Doc, FilePath, DocPath, JsonDict
from bdocs.building_docs import BuildingDocs
from cdocs.cdocs import Cdocs, BadDocPath
from cdocs.config import Config
from bdocs.writer import Writer
from bdocs.zipper import Zipper
from bdocs.walker import Walker
from cdocs.pather import Pather
from bdocs.mover import Mover
from bdocs.deleter import Deleter
from bdocs.rotater import Rotater
from bdocs.simple_rotater import SimpleRotater
from bdocs.simple_zipper import SimpleZipper
from cdocs.simple_pather import SimplePather
from bdocs.simple_writer import SimpleWriter
from bdocs.simple_mover import SimpleMover
from bdocs.simple_walker import SimpleWalker
from bdocs.bdocs_config import BdocsConfig
from bdocs.simple_deleter import SimpleDeleter
from bdocs.search_options import SearchOptions
from bdocs.printer import Printer


class Bdocs(BuildingDocs):

    def __init__(self, doc_root:FilePath, config:Optional[Config]=None):
        self._docs_root = doc_root
        cfg = BdocsConfig(None) if config is None else config
        self._config = cfg
        self._writer = SimpleWriter()
        self._walker = SimpleWalker()
        #self._mover = SimpleMover(cfg)
        self._deleter = SimpleDeleter()
        self._zipper = SimpleZipper(cfg)
        self._rotater = SimpleRotater()
        self._mover = SimpleMover(cfg, doc_root)
        self._pather = SimplePather(self._docs_root, cfg.get_config_path()) if cfg.pather is None else cfg.pather

    @property
    def mover(self) -> Mover:
        return self._mover

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

    def move_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        self.mover.move_doc(fromdoc,todoc)

    def copy_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        self.mover.copy_doc(fromdoc,todoc)

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

    # this doesn't really belong here because this Bdocs has
    # its own root and shouldn't be messing around with unzipping
    # another root
    def unzip_doc_tree(self, zipfile:FilePath) -> None:
        if not os.path.exists(zipfile):
            raise Exception(f"no file at {zipfile}")
        self.zipper.unzip_doc_tree(zipfile)

    # arguably this method belongs on Cdocs. not worried about that atm.
    def get_docs_with_titles(self, path:DocPath, options:Optional[SearchOptions]=None) -> Dict[str, DocPath]:
        cdocs = Cdocs(self.get_docs_root())
        tree = self.get_doc_tree()
        Printer().print_tree(tree)
        tokens = cdocs.get_tokens(path)
        Printer().print_tree(tokens)
        path = path.strip('/\\')
        pathnames = path.split("/")
        hashmark = self.config.get("filenames", "hashmark")
        results = {}
        print("results:")
        for k, v in tokens.items():
            print(f"\n   looking for: {k}:{v} with {pathnames[0]}")
            result = self._d( pathnames, tree , k, [], options )
            if result is not None:
                docpath = ""
                for _ in result[1]:
                    docpath += ("/"+_) if _.find(hashmark) == -1 else _
                results[v] = docpath
                print(f"   ...docpath: {docpath}, name: {v} ")
        return results

#
#
#  doesn't yet search below the original docpath, but it should.
#  see comment below.
#
    def _d( self, path:List[str], tree:JsonDict, searchkey:str, \
            currentpath:List[str], options:Optional[SearchOptions]=None, \
            recurse=True) -> Tuple[str, DocPath]:
        debugname = "no"
        if path == [] and options is not None and options.lookdown:
            self._load_paths_and_restart_d(path, tree, searchkey, currentpath, options)
        if path == []:
            return None

        thisname = path[0:1][0] if len(path) > 1 else path[0]
        if currentpath == [] or currentpath[-1] != thisname:
            currentpath.append(thisname)

        if searchkey == debugname:
            print(f"     thisname: {thisname}")
            print(f"     path: {path}")
            print(f"     currentpath: {currentpath}")

        for k, v in tree.items():
            if searchkey == debugname:
                print(f"     searchkey: {searchkey}, k:v: {k}:{v}")
            if k == searchkey and type(v).__name__ != 'dict':
                #
                # if filename matches the directory we don't add to the path
                #     given /app/home: home.xml == home so we don't add home to the path
                #
                hashmark = self.config.get("filenames", "hashmark")
                matches = v == thisname
                if searchkey == debugname:
                    print(f"     v == thisname: {thisname} ")
                    print(f"     v == thisname: {thisname} or == path0: {path[0]} ")
                    print(f"     _d.matches: matches: {matches}")
                    if (len(path) >= 1):
                        print(f"     {path}, {len(path)}, v, {path[0]}")
                    else:
                        print(f"     {path}, {len(path)}, v, {path}")
                    print(f"     _d.matches: v == {thisname}, matches: {matches}")
                if matches:
                    pass
                else:
                    currentpath.append(hashmark+v )
                return (searchkey, currentpath, v)
        for k,v in tree.items():
            if type(v).__name__ == 'dict' and k == path[0]:
                path = path[1:] if len(path) > 1 else path
                recurse = len(path)>1
                return self._d( path, v, searchkey, currentpath, \
                       options, recurse=recurse)
        return None

    # todo: get a list of paths going below the original docpath
    #       iterate over the list calling _d for each docpath
    #       return array of results to _d
    #       figure out how to _d can return an array
    def _load_paths_and_restart_d(self, path:List[str], tree:JsonDict, searchkey:str, \
            currentpath:List[str], options:SearchOptions ) -> Tuple[str,DocPath]:
        # we already went down so need to not loop
        options.lookdown = False
        return []




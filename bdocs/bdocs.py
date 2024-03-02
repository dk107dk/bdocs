import os
from  uuid import uuid4
import shutil
import logging
from typing import Optional, Union, List, Tuple, Dict
from cdocs.contextual_docs import Doc, FilePath, DocPath, JsonDict
from bdocs.building_docs import BuildingDocs
from bdocs.building_metadata import BuildingMetadata
from bdocs.multi_building_docs import MultiBuildingDocs
from cdocs.cdocs import Cdocs, BadDocPath
from cdocs.config import Config
from bdocs.writer import Writer
from bdocs.zipper import Zipper
from bdocs.walker import Walker
from cdocs.pather import Pather
from bdocs.rooter import Rooter
from bdocs.searcher import Searcher
from bdocs.indexer import Indexer
from bdocs.simple_null_searcher import SimpleNullSearcher
from bdocs.simple_null_indexer import SimpleNullIndexer
from bdocs.mover import Mover
from bdocs.deleter import Deleter
from bdocs.rotater import Rotater
from bdocs.simple_rooter import SimpleRooter
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

    def __init__(self, doc_root:FilePath, \
                 metadata:Optional[BuildingMetadata]=None, \
                 buildings:Optional[MultiBuildingDocs]=None):
        self._docs_root = doc_root
        self._block = buildings
        self._metadata = metadata
        if metadata is None:
            self._config = BdocsConfig(None)
        else:
            self._config = metadata.config
        self._writer = None
        self._walker = None
        self._deleter = None
        self._zipper = None
        self._rotater = None
        self._rooter = None
        self._mover = None
        self._pather = None
        self._indexer = None
        self._searcher = None

        self._use_writer = SimpleWriter
        self._use_walker = SimpleWalker
        self._use_deleter = SimpleDeleter
        self._use_zipper = SimpleZipper
        self._use_rotater = SimpleRotater
        self._use_rooter = SimpleRooter
        self._use_mover = SimpleMover
        self._use_pather = SimplePather
        self._use_searcher = SimpleNullSearcher
        self._use_indexer = SimpleNullIndexer
        #
        # TODO: should track_last_change be a feature?
        #

    @property
    def root_name(self):
        #i = self.docs_root.rindex("/")
        #return self.docs_root[i+1:]
        return self.config.get_matching_key_for_value("docs", self.docs_root)

    @property
    def docs_root(self):
        return self._docs_root

    def get_doc_root(self): # this method matches Cdocs
        return self.docs_root

    @property
    def block(self) -> MultiBuildingDocs:
        return self._block

    @property
    def config(self) -> Config:
        return self._config

    @property
    def metadata(self) -> BuildingMetadata:
        return self._metadata

# ---------------

    @property
    def cdocs(self) -> Cdocs:
        return Cdocs(self.get_docs_root())

    @property
    def mover(self) -> Mover:
        if self._mover is None:
            self._mover = self._use_mover(self.metadata, self)
        return self._mover

    @mover.setter
    def mover(self, mover:Mover):
        self._mover = mover

    @property
    def zipper(self) -> Zipper:
        if self._zipper is None:
            self._zipper = self._use_zipper(self.metadata, self)
        return self._zipper

    @zipper.setter
    def zipper(self, zipper:Zipper):
        self._zipper = zipper

    @property
    def deleter(self) -> Deleter:
        if self._deleter is None:
            self._deleter = self._use_deleter(self.metadata, self)
        return self._deleter

    @deleter.setter
    def deleter(self, deleter:Deleter):
        self._deleter = deleter

    @property
    def rotater(self) -> Rotater:
        if self._rotater is None:
            self._rotater = self._use_rotater(self.metadata, self)
        return self._rotater

    @rotater.setter
    def rotater(self, rotater:Rotater):
        self._rotater = rotater

    @property
    def rooter(self) -> Rooter:
        if self._rooter is None:
            self._rooter = self._use_rooter(self.metadata, self)
        return self._rooter

    @rooter.setter
    def rooter(self, rooter:Rooter) -> None:
        self._rooter = rooter

    @property
    def writer(self) -> Writer:
        if self._writer is None:
            self._writer = self._use_writer(self.metadata, self)
        return self._writer

    @writer.setter
    def writer(self, writer:Writer) -> None:
        self._writer = writer

    @property
    def walker(self) -> Walker:
        if self._walker is None:
            self._walker = self._use_walker(self.metadata, self)
        return self._walker

    @walker.setter
    def walker(self, walker:Walker) -> None:
        self._walker = walker

    @property
    def pather(self) -> Pather:
        if self._pather is None:
            self._pather = self._use_pather(self.metadata, self)
        return self._pather

    @pather.setter
    def pather(self, pather:Pather) -> None:
        self._pather = pather

    @property
    def searcher(self) -> Searcher:
        if self._searcher is None:
            self._searcher = self._use_searcher(self.metadata, self)
        return self._searcher

    @searcher.setter
    def searcher(self, searcher:Searcher) -> None:
        self._searcher = searcher

    @property
    def indexer(self) -> Indexer:
        if self._indexer is None:
            self._indexer = self._use_indexer(self.metadata, self)
        return self._indexer

    @indexer.setter
    def indexer(self, indexer:Indexer) -> None:
        self._indexer = indexer

# ------------------

    def init_root(self):
        root = self.get_docs_root()
        self.rooter.init_root()

    def delete_root(self):
        self.rooter.delete_root()

    def get_docs_root(self) -> FilePath:
        return self._docs_root

    def _track_last_change(self) -> None:
        cdocs = self.cdocs
        cdocs.track_last_change = True
        cdocs.set_last_change()

    def put_doc(self, path:DocPath, doc:Union[bytes,Doc]) -> None:
        filepath:FilePath = self.pather.get_full_file_path(path)
        logging.info(f"Bdocs.put_doc: path: {path}, filepath: {filepath} ")
        if type(doc) == 'bytes':
            bs = doc
        else:
            bs = doc.encode()
        logging.info(f"Bdocs.put_doc: path: {path}, filepath: {filepath} ")
        self.writer.write(filepath, bs)
        self.indexer.index_doc(path, doc)
        self._track_last_change()

    def move_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        self.mover.move_doc(fromdoc,todoc)
        self._track_last_change()

    def copy_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        self.mover.copy_doc(fromdoc,todoc)
        self._track_last_change()

    def delete_doc(self, path:DocPath) -> None:
        filepath:FilePath = self.pather.get_full_file_path(path)
        self.deleter.delete(filepath)
        self.indexer.remove_doc(path)
        self._track_last_change()

    def delete_doc_tree(self, path:DocPath) -> None:
        filepath = self.get_dir_for_docpath(path)
        self.deleter.delete_doc_tree(filepath)
        self._track_last_change()

    def get_dir_for_docpath(self, path:DocPath) -> FilePath:
        logging.info(f"get_dir_for_docpath: root: {self.get_docs_root()} path: {path}")
        filepath:FilePath = self.pather.get_full_file_path(path)
        logging.info(f"bdocs.get_dir_for_docpath: filepath: {filepath} from path: {path}")
        if filepath.find(".") > -1:
            filepath = filepath[0:filepath.rindex(".")]
        return filepath

    def doc_exists(self, path:DocPath) -> bool:
        filepath:FilePath = self.pather.get_full_file_path(path)
        return os.path.exists(filepath)

    def get_doc_tree(self) -> JsonDict:
        return self.walker.get_doc_tree()

    def zip_doc_tree(self) -> FilePath:
        dir = self.get_dir_for_docpath("/")
        return self.zipper.zip(dir)

    #
    # -------------- suspect code vvvvv
    #
    # arguably this method belongs on Cdocs. not worried about that atm.
    def get_docs_with_titles(self, path:DocPath, options:Optional[SearchOptions]=None) -> Dict[str, DocPath]:
        cdocs = Cdocs(self.get_docs_root())
        tree = self.get_doc_tree()
        #Printer().print_tree(tree)
        tokens = cdocs.get_tokens(path)
        #Printer().print_tree(tokens)
        path = path.strip('/\\')
        pathnames = path.split("/")
        hashmark = self.config.get("filenames", "hashmark")
        results = {}
        #print("results:")
        for k, v in tokens.items():
            #print(f"\n   looking for: {k}:{v} with {pathnames[0]}")
            result = self._d( pathnames, tree , k, [], options )
            if result is not None:
                docpath = ""
                for _ in result[1]:
                    docpath += ("/"+_) if _.find(hashmark) == -1 else _
                results[v] = docpath
                #print(f"   ...docpath: {docpath}, name: {v} ")
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




import abc
from typing import Union, Optional, Dict, List
from bdocs.search_options import SearchOptions
from bdocs.multi_building_docs import MultiBuildingDocs
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs import Bdocs
from bdocs.tree_util import TreeUtil
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.cdocs import Cdocs,BadDocPath
from bdocs.zipper import Zipper
from bdocs.simple_zipper import SimpleZipper
import logging
import os

class Block(MultiBuildingDocs):


    def __init__(self, metadata:BuildingMetadata):
        self._metadata = metadata
        self._keyed_bdocs = { k : Bdocs(v, metadata, self) for k,v in metadata.keyed_roots.items() }
        self._bdocs = [ v for k,v in self._keyed_bdocs.items() ]
        self._zipper = SimpleZipper(self.metadata, None)

#-------------

    @property
    def config(self):
        return self._config

    @property
    def metadata(self):
        return self._metadata

    @property
    def zipper(self) -> Zipper:
        return self._zipper

#-------------

    def get_root(self, rootname:str) -> Bdocs:
        return self._keyed_bdocs.get(rootname)

    def unzip_doc_tree(self, zipfile:FilePath) -> None:
        if not os.path.exists(zipfile):
            raise Exception(f"no file at {zipfile}")
        self.zipper.unzip_doc_tree(zipfile)

    def join_trees(self, rootnames:List[str]) -> JsonDict:
        trees = [ self._keyed_bdocs[root].get_doc_tree() for root in rootnames]
        return self._join_trees(trees)

    def _join_trees(self, trees:List[JsonDict]) -> JsonDict:
        overlaps = {}
        addright = 0
        addleft = 0
        overlap = 0
        result = trees[0]
        counts = {}
        tu = TreeUtil()
        for treenum in range(1,len(trees)):
            one = trees[treenum]
            result = tu.union( one, result, overlap=overlaps, counts=counts)
            r = counts.get('add_right')
            addright = addright + r if r is not None else addright
            r = counts.get('overlap')
            overlap = overlap + r if r is not None else overlap
            r = counts.get('add_left')
            addleft = addleft + r if r is not None else addleft
        logging.info(f"Block.join_trees. adds: al,ol,ar: {addleft}, {overlap}, {addright}")
        logging.info(f"Block.join_trees. overlaps: {overlaps}")
        logging.info(f"Block.join_trees. result: {result}")
        return result

    def list_trees(self, rootnames:List[str], add_root_names:bool=True ) -> List[str]:
        tree = None
        treelist = []
        if len(rootnames) == 1:
            bdocs = self.get_root(rootnames[0])
            if bdocs is None:
                logging.info(f"Block.list_trees: rootnames[0]: {rootnames[0]} not found")
            tree = bdocs.get_doc_tree()
            logging.info(f"Block.list_trees: tree for rootname: {rootnames[0]}: {tree}")
            treelist = self._tree_to_list(tree, [], [rootnames[0]] if add_root_names else [] )
        else:
            for root in rootnames:
                bdocs = self.get_root(root)
                tree = bdocs.get_doc_tree()
                tl = self._tree_to_list(tree, [], [root] if add_root_names else [] )
                treelist += tl
        treelist.sort()
        return treelist

    def _tree_to_list(self, tree:JsonDict, treelist:List[str]=[], path:List[str]=[]) -> List[str]:
        for k,v in tree.items():
            path.append(k)
            if type(v).__name__ == 'dict':
                treelist = self._tree_to_list(v, treelist, path)
            else:
                treelist.append("/".join(path))
            path = path[0:-1]
        return treelist

    def put_doc(self, rootname:str, path:DocPath, doc:Union[bytes,Doc]) -> None:
        self.get_root().put_doc(path, doc)

    def move_doc(self, fromrootname:str, fromdoc:DocPath, torootname:str, todoc:DocPath) -> None:
        cdocs = Cdocs(fromrootname, self.metadata.config)
        doc = cdocs.get_doc(fromdoc)
        if doc is None:
            raise BadDocPath(f"No such doc: {fromdoc}")
        self.put_doc(torootname, todoc, doc)
        self.delete_doc([fromrootname], fromdoc)

    def copy_doc(self, fromrootname:str, fromdoc:DocPath, torootname:str, todoc:DocPath) -> None:
        cdocs = Cdocs(fromrootname, self.metadata.config)
        doc = cdocs.get_doc(fromdoc)
        if doc is None:
            raise BadDocPath(f"No such doc: {fromdoc}")
        self.put_doc(torootname, todoc, doc)

    def delete_doc(self, rootnames:List[str], path:DocPath) -> None:
        for rootname in rootnames:
            self.get_root(rootname).delete_doc(path)

    def delete_doc_tree(self, rootnames:List[str], path:DocPath) -> None:
        for rootname in rootnames:
            self.get_root(rootname).delete_doc_tree(path)

    def get_dir_for_docpath(self, rootname:str, path:DocPath) -> FilePath:
        return self.get_root(rootname).get_dir_for_docpath(path)

    def doc_exists(self, rootnames:List[str], path:DocPath) -> bool:
        """ docpath must exist in all roots """
        for rootname in rootnames:
            if not self.get_root(rootname).doc_exists(path):
                return False
        return True

    def get_doc_tree(self, rootname:str) -> JsonDict:
        return self.get_root(rootname).get_doc_tree()

    def zip_doc_tree(self, rootname:str) -> FilePath:
        return self.get_root(rootname).zip_doc_tree()


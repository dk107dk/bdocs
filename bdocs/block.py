import abc
from typing import Union, Optional, Dict, List
from bdocs.search_options import SearchOptions
from bdocs.multi_building_docs import MultiBuildingDocs
from bdocs.bdocs import Bdocs
from bdocs.tree_util import TreeUtil
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.context import ContextMetaData

class Block(MultiBuildingDocs):


    def __init__(self, metadata:ContextMetaData):
        self._metadata = metadata
        self._keyed_bdocs = { k : Bdocs(v, metadata.config, self) for k,v in metadata.keyed_roots.items() }
        self._bdocs = [ v for k,v in self._keyed_bdocs.items() ]

    @property
    def config(self):
        return self._config

    @property
    def metadata(self):
        return self._metadata

    def join_trees(self, rootnames:List[str]) -> JsonDict:
        print(f"Block.join_trees")
        tu = TreeUtil()
        trees = [ self._keyed_bdocs[root].get_doc_tree() for root in rootnames]
        overlaps = {}
        addright = 0
        addleft = 0
        overlap = 0
        result = trees[0]
        counts = {}
        for treenum in range(1,len(trees)):
            one = trees[treenum]
            result = tu.union( one, result, overlap=overlaps, counts=counts)
            r = counts.get('add_right')
            addright = addright + r if r is not None else addright
            r = counts.get('overlap')
            overlap = overlap + r if r is not None else overlap
            r = counts.get('add_left')
            addleft = addleft + r if r is not None else addleft
        print(f"Block.join_trees. adds: al,ol,ar: {addleft}, {overlap}, {addright}")
        print(f"Block.join_trees. overlaps: {overlaps}")
        print(f"Block.join_trees. result: {result}")
        return result

    def put_doc(self, rootname:str, path:DocPath, doc:Union[bytes,Doc]) -> None:
        pass

    def move_doc(self, fromrootname:str, fromdoc:DocPath, torootname:str, todoc:DocPath) -> None:
        pass

    def copy_doc(self, fromrootname:str, fromdoc:DocPath, torootname:str, todoc:DocPath) -> None:
        pass

    def delete_doc(self, rootnames:List[str], path:DocPath) -> None:
        pass

    def delete_doc_tree(self, rootnames:List[str], path:DocPath) -> None:
        pass

    def get_dir_for_docpath(self, rootname:str, path:DocPath) -> FilePath:
        pass

    def doc_exists(self, rootnames:List[str], path:DocPath) -> bool:
        pass

    def get_doc_tree(self, rootname:str) -> JsonDict:
        pass

    def zip_doc_tree(self, rootname:str) -> FilePath:
        pass




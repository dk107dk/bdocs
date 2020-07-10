from application.roots.doc_root_management import DocRootManagement
from bdocs.building_metadata import BuildingMetadata
from bdocs.block import Block
from cdocs.context import Context
from typing import Dict, List, Type, Union, Tuple, Optional, NewType

class AdocsDocpath(object):

    @classmethod
    def get_tree(cls, id:int, name:str) -> Dict:
        mgmt = DocRootManagement()
        uid,tid,pid = cls._get_uid_tid_pid(id)
        config = mgmt.get_config_of(uid, tid, pid)
        metadata = BuildingMetadata(config)
        building = Block(metadata)
        tree = building.get_doc_tree(name)
        print(f"tree at {tree} found ")
        if tree is None:
            tree = "get_doc_tree returned None"
        return tree

    @classmethod
    def get_docs_at_path(cls, id:int, docpath:str, roots:Optional[List[str]]=None) -> str:
        mgmt = DocRootManagement()
        uid,tid,pid = cls._get_uid_tid_pid(id)
        config = mgmt.get_config_of(uid, tid, pid)
        print(f"Adocs.get_docs_at_path: id: {id}, docpath: {docpath}, roots: {roots} with config: {config.get_config_path()}")
        metadata = BuildingMetadata(config)
        context = Context(metadata)
        doc = ""
        if roots is None:
            print(f"Adocs.get_docs_at_path: roots is none. get_doc on context for any root")
            doc = context.get_doc(docpath)
        else:
            print(f"Adocs.get_docs_at_path: limited to {roots}")
            for root in roots:
                info = metadata.get_root_info(root)
                print(f"app.docs: root: {root}, info: {info}, transform: {info.transform}")
                if not info.transform :
                    cdocs = context.keyed_cdocs[root]
                    cdocs.track_last_change = False
                    cdocs.transformer = SimpleNullTransformer(cdocs)
            doc = context.get_doc_from_roots(roots,docpath)
        print(f"cdocs at {docpath} found {doc} ")
        if doc is None:
            pass #doc = f"Doc not found at docpath {docpath}. There is no 'not found' doc configured."
        return doc

    @classmethod
    def get_doc_at_path_as_json(cls, id:int, docpath:str, roots:Optional[List[str]]=None) -> str:
        doc = cls.get_docs_at_path(id, docpath, roots)
        if doc is not None:
            try:
                json.load(doc)
            except:
                doc = { "doc": doc }
        return doc

    @classmethod
    def get_labels_at_path(cls, id:int, docpath:str, roots:Optional[List[str]]=None, recurse:bool=True) -> str:
        return cls._get_x_at_path("labels", id, docpath, roots, recurse)

    @classmethod
    def get_tokens_at_path(cls, id:int, docpath:str, roots:Optional[List[str]]=None, recurse:bool=True) -> str:
        return cls._get_x_at_path("tokens", id, docpath, roots, recurse)

    @classmethod
    def _get_x_at_path(cls, x:str, id:int, docpath:str, roots:Optional[List[str]]=None, recurse:bool=True) -> str:
        mgmt = DocRootManagement()
        uid,tid,pid = cls._get_uid_tid_pid(id)
        config = mgmt.get_config_of(uid, tid, pid)
        print(f"Adocs.get_docs_at_path: id: {id}, docpath: {docpath}, roots: {roots} with config: {config.get_config_path()}")
        metadata = ContextMetadata()
        context = Context(metadata)
        doc = ""
        if x == "tokens":
            if roots is None:
                doc = context.get_tokens(docpath, recurse)
            else:
                doc = context.get_tokens_from_roots(roots, docpath, recurse)
        elif x == "labels":
            if roots is None:
                doc = context.get_labels(docpath, recurse)
            else:
                doc = context.get_labels_from_roots(roots, docpath, recurse)
        print(f"cdocs at {docpath} found ")
        return doc




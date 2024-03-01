import os
from cdocs.contextual_docs import FilePath, JsonDict
from bdocs.building_metadata import BuildingMetadata
from bdocs.walker import Walker
from cdocs.cdocs import BadDocPath
import logging

class SimpleWalker(Walker):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    # can't type hint Bdocs on the bdocs arg because it would
    # be a circular import ref.
    def get_doc_tree(self) -> JsonDict:
        filepath = self._bdocs.docs_root
        logging.debug(f"SimpleWalker.get_doc_tree: filepath: {filepath}")
        jsondict = JsonDict(dict())
        if not os.path.isdir(filepath):
            raise BadDocPath(f"{filepath} is not a root directory")
        self._collect_tree(filepath, jsondict)
        return jsondict

    def _collect_tree(self, apath:FilePath, jsondict:JsonDict) -> None:
        items = os.listdir(apath)
        for item in items:
            itempath = os.path.join(apath,item)
            if os.path.isfile(itempath):
                # skip files starting with '.' -- e.g. .DS_Store
                if item[0:1] == '.':
                    pass
                else:
                    docname = item
                    ext = docname.find(".")
                    if ext > -1:
                        docname = item[0:ext]
                    jsondict[item] = docname
            else:
                subtree = dict()
                jsondict[item] = subtree
                self._collect_tree(itempath, subtree)

    def subtract(self, subtractthis:JsonDict, fromthat:JsonDict) -> JsonDict:
        ft = self._clone(fromthat)
        return self._subtract(subtractthis, ft)

    def _clone(self, adict:JsonDict) -> JsonDict:
        newdict = {}
        for k,v in adict:
            if self._dict(v):
                newdict[k] = self._clone(v)
            else:
                newdict[k] = v
        return newdict

    def _isdict(self, something):
        return type(something).__name__ == 'dict'

    def _subtract(self, subtractthis:JsonDict, fromthat:JsonDict ) -> JsonDict:
        for k,v in subtractthis:
            if self._dict(v) and k in fromthat and self._dict(fromthat[k]):
                return self._subtract(v, fromthat[k])
            else:
                fromthat.pop(k)
        return fromthat





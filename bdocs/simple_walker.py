import os
from cdocs.contextual_docs import FilePath, JsonDict
from bdocs.walker import Walker
from cdocs.cdocs import BadDocPath
import logging

class SimpleWalker(Walker):

    # can't type hint Bdocs on the bdocs arg because it would
    # be a circular import ref.
    def get_doc_tree(self, bdocs) -> JsonDict:
        filepath = bdocs.get_dir_for_docpath("/")
        jsondict = JsonDict(dict())
        if not os.path.isdir(filepath):
            raise BadDocPath(f"{filepath} is not a root directory")
        jsondict = self._collect_tree(filepath, jsondict)
        return jsondict

    def _collect_tree(self, apath:FilePath, jsondict) -> JsonDict:
        items = os.listdir(apath)
        for item in items:
            itempath = os.path.join(apath,item)
            if os.path.isfile(itempath):
                if item[0:1] == '.':
                    pass
                else:
                    docname = item
                    ext = docname.find(".")
                    if ext > -1:
                        docname = item[0:ext]
                    jsondict[docname] = item
            else:
                jsondict[item] = dict()
                self._collect_tree( itempath, jsondict[item])
        return jsondict






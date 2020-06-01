from cdocs.contextual_docs import JsonDict
import logging
from typing import Dict, List, Tuple

class TreeUtil(object):
    """ methods that act on JsonDict as if they were immutable """

    def clone(self, adict:JsonDict) -> JsonDict:
        newdict = {}
        for k,v in adict.items():
            if self._dict(v):
                newdict[k] = self.clone(v)
            else:
                newdict[k] = v
        return newdict

    def subtract(self, subtractthis:JsonDict, fromthat:JsonDict) -> JsonDict:
        ft = self.clone(fromthat)
        self._subtract(subtractthis, ft)
        return ft

    # if you want to merge more than two trees and want the overlaps
    # to be complete pass in an identifier as first element of path.
    # if passing in path the identifier should indicate the first
    # argument tree. therefore, if merging multiple trees always put
    # the next tree as first argument. see unit test.
    def union( self, one:JsonDict, two:JsonDict, overlap:Dict={}, path:List=[], counts:Dict={}) -> JsonDict:
        """
        one and two: the trees to union.
        overlaps: captures any values that are not returned in the unioned tree.
        path: a list of path names that are used to point to items in the trees.
           the first item in paths can serve to indicate the source tree.
        """
        three = self.clone(one)
        logging.info(f"TreeUtil.union: tree one: {three}, tree two: {two}, overlap: {overlap}, path: {path}")
        self._union(three, two, overlap, path, counts)
        return three

    def size(self, tree:Dict) -> int:
        n = 0
        for k,v in tree.items():
            n +=1
            if self._dict(v):
                n+= self.size(v)
        return n

# -----------------

    # when conflicts items in two replace items in one and the value replaced goes to overlaps
    def _union(self, one:JsonDict, two:JsonDict, overlap:JsonDict, path:List, counts:Dict) -> JsonDict:
        #
        # everything from two that is either
        #    not in one, or
        #    overlaps one
        #
        for k,v in two.items():
            if self._dict(v):
                item = one.get(k)
                if item is None:
                    item = {}
                    self._counts(counts, "add_right", 1, (k,item))
                else:
                    self._counts(counts, "overlap", 1, (k,item))
                    if not self._dict(item):
                        overlap[self._pk(path,k)] = str(item)
                        item = {}
                one[k] = item
                path.append(k)
                self._union(item,v,overlap,path,counts)
            else: # not a dict
                item = one.get(k)
                if item is None:
                    self._counts(counts, "add_right", 1, (k,item) )
                else:
                    overlap[ self._pk(path,k) ] = str(item)
                    n = 1
                    if self._dict(item):
                        n = self.size(item)
                    self._counts(counts, "overlap", n, (k,item))
                one[k] = v
        #
        # everything else in one
        #
        for k,v in one.items():
            if not k in two:
                n = 1
                if self._dict(v):
                    n = self.size(v) + 1
                self._counts(counts, "add_left", n, (k,v))
        if len(path) > 0:
            path.pop()

    def _counts(self, counts:Dict, key:str, cnt:int, t:Tuple[str,any]) -> None:
        n = counts.get(key)
        if n is not None:
            cnt += n
        counts[key] = cnt
        logging.info(f"TreeUtil._counts: {key}={cnt} for tuple: {t}")

    def _pk(self, path:List, key:str) -> str:
        sp = ".".join(path)
        sp = sp + "." + key if len(sp) > 0 else key
        return sp

    def _subtract(self, subtractthis:JsonDict, fromthat:JsonDict ) -> None:
        for k,v in subtractthis.items():
            if self._dict(v) and k in fromthat and self._dict(fromthat[k]):
                return self._subtract(v, fromthat[k])
            else:
                self._rm(fromthat, k)

    def _dict(self, something):
        return type(something).__name__ == 'dict'

    def _rm(self, adict:Dict, key:str) -> None:
        if adict.get(key) is not None:
            adict.pop(key)


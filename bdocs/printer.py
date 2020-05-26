from cdocs.contextual_docs import JsonDict

class Printer(object):
    """
    Printer knows how to print things nicely.
    """

    def print_tree(self, tree:JsonDict) -> None:
        s = self._print_tree(tree, "", 0)
        print(s)

    def _print_tree(self, tree:JsonDict, s:str, pad:int ) -> str:
        s = "{\n"
        pad+=1
        for k,v in tree.items():
            s += self._pad(pad) +  f"'{k}':"
            if type(v).__name__ == 'dict':
                s += self._print_tree(v, s, pad)
            else:
                s += f"'{v}',\n"
        pad-=1
        s += self._pad(pad) + "}\n"
        return s

    def _pad(self, pad:int) -> str:
        s = ""
        for i in range(pad):
            s += " "
        return s

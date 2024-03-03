from cdocs.repl import Repl
from bdocs.printer import Printer
from bdocs.bdocs import Bdocs
from bdocs.building_metadata import BuildingMetadata
import traceback


class Brepl(Repl):
    def __init__(self):
        print("\n------------------------------")
        print("Brepl. a simple cli for bdocs!")
        print("------------------------------\n")
        super().__init__()
        self._add_additional_commands()
        self._last_root = None

    def _get_root(self):
        root = None
        if self._last_root:
            root = self._input(f"which root? ([return] for '{self._last_root}') ")
            if root == "":
                root = self._last_root
            self._response(f"using {root}")
        else:
            root = self._input("which root? ")
        self._last_root = root
        return root

    def _add_additional_commands(self):
        super().commands["tree"] = self.tree
        super().commands["move"] = self.move
        super().commands["put"] = self.put
        super().commands["delete"] = self.delete
        super().commands["zip"] = self.zip
        super().commands["last_change"] = self.last_change

    def tree(self):
        root = self._get_root()
        try:
            metadata = BuildingMetadata()
            cdocs = self._context.keyed_cdocs.get(root)
            bdocs = Bdocs(cdocs._docs_path, metadata)
            docs = bdocs.get_doc_tree()
            printer = Printer()
            printer.print_tree(docs)
        except Exception as e:
            print(f"Error: {e}")
        return True

    def move(self):
        root = self._get_root()
        try:
            from_path = self._input("from? ")
            to = self._input("to? ")
            metadata = BuildingMetadata()
            cdocs = self._context.keyed_cdocs.get(root)
            bdocs = Bdocs(cdocs._docs_path, metadata)
            if not bdocs.doc_exists(from_path):
                self._response(from_path)
            bdocs.move_doc(from_path, to)
        except Exception as e:
            print(f"Error: {e}")
        return True

    def put(self):
        root = self._get_root()
        try:
            at = self._input("put where? ")
            data = self._input("put what? ")
            metadata = BuildingMetadata()
            cdocs = self._context.keyed_cdocs.get(root)
            bdocs = Bdocs(cdocs._docs_path, metadata)
            bdocs.put_doc(at, data)
        except Exception as e:
            print(f"Error: {e}")
        return True

    def delete(self):
        root = self._get_root()
        try:
            at = self._input("delete what? ")
            metadata = BuildingMetadata()
            cdocs = self._context.keyed_cdocs.get(root)
            bdocs = Bdocs(cdocs._docs_path, metadata)
            bdocs.delete_doc(at)
        except Exception as e:
            print(f"Error: {e}")
        return True

    def zip(self):
        root = self._get_root()
        try:
            metadata = BuildingMetadata()
            cdocs = self._context.keyed_cdocs.get(root)
            bdocs = Bdocs(cdocs._docs_path, metadata)
            path = bdocs.zip_doc_tree()
            self._response(f"zipped {root} to {path}")
        except Exception as e:
            print(f"Error: {e}")
        return True

    def last_change(self):
        root = self._get_root()
        try:
            cdocs = self._context.keyed_cdocs.get(root)
            cdocs.track_last_change = True
            cdocs._last_change = None  # should be a better way!
            change = cdocs.get_last_change()
            self._response(f"last change to {root} at {change}")
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
        return True

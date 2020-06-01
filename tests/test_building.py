from bdocs.tree_util import TreeUtil
import unittest
from bdocs.multi_building_docs import MultiBuildingDocs
from bdocs.block import Block
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.context import ContextMetaData

class BlockTests(unittest.TestCase):

    noise = True
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def test_join(self):
        self._print(f"BlockTests.test_join")
        metadata = ContextMetaData()
        building = Block(metadata)
        tree = building.join_trees(["public", "internal", "images"])
        self._print(f"BlockTests.test_join: tree: {tree}")

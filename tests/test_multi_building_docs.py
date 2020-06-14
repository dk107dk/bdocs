from bdocs.tree_util import TreeUtil
import unittest
from bdocs.multi_building_docs import MultiBuildingDocs
from bdocs.block import Block
from cdocs.contextual_docs import FilePath, DocPath, Doc, JsonDict
from cdocs.context import ContextMetadata
from bdocs.bdocs_config import BdocsConfig
from bdocs.building_metadata import BuildingMetadata
import shutil
import os

BASE:FilePath = "/Users/davidkershaw/dev/bdocs"
PATH:FilePath = BASE + "/docs/example"

class BlockTests(unittest.TestCase):

    noise = False
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def test_unzip_doc_tree(self):
        config = BdocsConfig()
        metadata = BuildingMetadata(config)
        building = Block(metadata)
        shutil.copyfile(BASE+"/tests/resources/test.zip", BASE+"/tests/resources/____.zip" )
        building.unzip_doc_tree( BASE+"/tests/resources/____.zip" )
        b = os.path.exists( BASE + "/docs/test")
        self.assertEqual(b, True, msg=f'{BASE + "/docs/test"} must exist')
        if b:
            shutil.rmtree(BASE + "/docs/test")
            config.remove_from_config("docs", "test")

    def test_join(self):
        self._print(f"BlockTests.test_join")
        metadata = ContextMetadata()
        building = Block(metadata)
        tree = building.join_trees(["internal", "images"])
        self._print(f"BlockTests.test_join: tree: {tree}")
        treestr = str(tree)
        self._print("BlockTests.test_join: treestr: {treestr}")
        self.assertNotEqual( -1, treestr.find("3-copy.png"), msg=f"must include: 3-copy.png")
        self.assertNotEqual( -1, treestr.find("tokens.json"), msg=f"must include: tokens.json")
        self.assertNotEqual( -1, treestr.find("404.xml"), msg=f"must include: 404.xml")
        self.assertNotEqual( -1, treestr.find("delete_assignee.xml"), msg=f"must include: delete_assignee.xml")

    def test_tree_list(self):
        self._print(f"BlockTests.test_tree_list")
        metadata = ContextMetadata()
        building = Block(metadata)
        treelist = building.list_trees(["public", "internal", "images"])
        self._print(f"BlockTests.test_tree_list: treelist: {treelist}")
        for line in treelist:
            self._print(f"   {line}")
        # test for a selection of paths expected
        paths = []
        paths.append("public/app/home/teams/todos/assignee/assignee.xml")
        paths.append("public/app/home/teams/tokens.json")
        paths.append("public/app/home/teams/link_check.html")
        paths.append("internal/404.xml")
        paths.append("internal/app/home/teams/delete_assignee.xml")
        paths.append("images/app/home/teams/todos/tokens.json")
        paths.append("images/app/home/teams/todos/3-copy.png")
        for path in paths:
            self.assertIn(path, treelist, msg=f"path not in treelist: {path}")


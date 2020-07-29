from application.app_config import AppConfig
from bdocs.bdocs_config import BdocsConfig
from bdocs.tree_util import TreeUtil
import unittest

class TreeUtilTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setting up TreeUtilTests")
        AppConfig.setTesting()

    noise = BdocsConfig().get("testing", "TreeUtilTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "TreeUtilTests") == "off"

    def test_clone(self):
        self._print(f"TreeUtilTests.test_clone")
        if self._off(): return
        tu = TreeUtil()
        one = { "a":"a", "b":"b", "m":{"n":"n", "o":"o"} }
        two = tu.clone(one)
        self._print(f"TreeUtilTests.test_clone: two: {two}")
        self.assertNotEqual( True, one is two, msg=f"the 'two' result object must be new, not the 'one' target object")
        self.assertEqual( 3, len(two), msg=f"size of cloned dict must be 3, not {two}")
        em = two.get("m")
        self.assertIsNotNone(em, msg=f"the 'm' key must exist in {two}")

    def test_size(self):
        self._print(f"TreeUtilTests.test_clone")
        if self._off(): return
        tu = TreeUtil()
        tree = { "b":"BBB", "x":"x", "y":"y", "z":{"1":"1", "2":"2"}}
        n = tu.size(tree)
        self._print(f"TreeUtilTests.test_size: n: {n} vs len: {len(tree)}")
        self.assertEqual(6, n, msg="size must be 6, not {n}")

    def test_union(self):
        self._print(f"TreeUtilTests.test_clone")
        if self._off(): return
        tu = TreeUtil()
        one = { "a":"a", "b":"b",   "m":{"n":"n", "o":"o"},                       "z":{"1":"one","2":"two"} }
        two = {          "b":"BBB",                         "x":"x", "y":"y",     "z":{"1":"1"}}
        three = { "1":"1", "2":"2", "3":"3", "m":{"n":{"4":"4"}}}
        self._print(f"TreeUtilTests.test_union: one: {one}")
        self._print(f"TreeUtilTests.test_union: two: {two}")
        overlap1 = {}
        #
        result1 = tu.union(one,two, overlap=overlap1)
        self._print(f"TreeUtilTests.test_union: result1: {result1}")
        self._print(f"TreeUtilTests.test_union: overlap1: {overlap1}")
        self.assertNotEqual( True, (result1 is two or three is one ), msg=f"the 'result1' result object must be new")
        self.assertEqual( 6, len(result1), msg=f"size of new dict must be 6, not {three}")
        zee = result1.get("z")
        self.assertIsNotNone(zee, msg=f"the 'z' key must exist in {result1}")
        self.assertIn( "b", overlap1, msg=f"'b' must be in {overlap1}")
        path = ["one"]
        overlap2 = {}
        counts2 = {}
        #
        result2 = tu.union(one, two, path=path, overlap=overlap2, counts=counts2)
        self._print(f"TreeUtilTests.test_union: result2: {result2}, overlap: {overlap2}, counts2: {counts2}")
        self.assertIn('one.z.1', overlap2, msg=f"overlap2 must include 'one.z.1'")
        path = ["three"]
        counts2 = {}
        #
        result3 = tu.union(three,result2,path=path, overlap=overlap2, counts=counts2)
        self._print(f"TreeUtilTests.test_union: result3: {result3}, overlap: {overlap2}, counts2: {counts2}")
        self.assertIn('three.m.n', overlap2, msg=f"overlap2: {overlap2} must include 'three.m.n'")
        self.assertEqual(counts2["add_left"], 3, msg=f"left tree must have contributed 3, not {counts2}")
        self.assertEqual(counts2["add_right"], 8, msg=f"right tree must have contributed 8, not {counts2}")
        self.assertEqual(counts2["overlap"], 2, msg=f"overlap must have contributed 2, not {counts2}")

    def test_subtract(self):
        self._print(f"TreeUtilTests.test_subtract")
        if self._off(): return
        tu = TreeUtil()
        subthis  = { "a":"a", "b":"b", "m":{"n":"n", "o":"o"} }
        fromthat = { "a":"a", "b":"b", "c":"c", "d":"d" }
        fromthat['m'] = {"o":"o", "p":"p"}
        self._print(f'TreeUtilTests.test_subtract: subtract this: {subthis}')
        self._print(f'TreeUtilTests.test_subtract: from that: {fromthat}')
        result = tu.subtract(subthis, fromthat)
        self._print(f'TreeUtilTests.test_subtract: result: {result}')
        self.assertNotEqual( True, result is fromthat, msg=f"the result object must be new, not the 'fromthat' target object")
        self.assertIn( "c", result, msg=f"'c' must be in {result}")
        self.assertIn( "d", result, msg=f"'d' must be in {result}")
        self.assertNotIn( "a", result, msg=f"'a' must not be in {result}")
        self.assertNotIn( "b", result, msg=f"'b' must not be in {result}")


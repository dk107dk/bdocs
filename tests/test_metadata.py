import unittest
from cdocs.context import ContextMetadata
from bdocs.bdocs_config import BdocsConfig
from bdocs.building_metadata import BuildingMetadata, RootInfo

class MetadataTests(unittest.TestCase):

    noise = BdocsConfig().get("testing", "MetadataTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def off(self) -> bool:
        return BdocsConfig().get("testing", "MetadataTests") == "off"

    def test_root_info(self):
        self._print(f"MetadataTests.test_root_info")
        if self.off(): return
        config = BdocsConfig()
        metadata = BuildingMetadata(config)
        rootinfo = metadata.get_root_info("public")
        self._print(f"MetadataTests.test_root_info: rootinfo for public: {rootinfo}")
        self.assertIsNotNone( rootinfo, msg=f"no root info for public!")
        self.assertEqual( rootinfo.name, "public", msg=f"rootinfo.name must be public, not {rootinfo.name}")
        self.assertIn("cdocs", rootinfo.accepts, msg=f"rootinfo must accept 'cdocs': {rootinfo.accepts}")
        self.assertIn("xml", rootinfo.formats, msg=f"rootinfo must use 'xml': {rootinfo.formats}")
        features = metadata.features.get("public")
        self.assertIsNotNone(features, msg=f"features of 'public' must not be None")
        #search,git,transform
        self.assertEqual( len(features), 3, msg=f"'public' must have 3 features, not {len(features)}")

        features = metadata.features.get("json")
        self._print(f"MetadataTests.test_root_info: features of json: {features}")
        self.assertIsNotNone(features, msg=f"features of 'json' must not be None")
        #transform
        self.assertEqual( len(features), 1, msg=f"'json' must have 1 features, not {len(features)}")
        self.assertIn("transform", features, msg=f"'json' must have 'transform': {features}")



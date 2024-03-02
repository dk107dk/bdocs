import unittest
from cdocs.context import ContextMetadata
from bdocs.bdocs_config import BdocsConfig
from bdocs.building_metadata import BuildingMetadata
import logging

class MetadataTests(unittest.TestCase):



    def test_root_info(self):
        logging.info(f"MetadataTests.test_root_info")
        config = BdocsConfig()
        metadata = BuildingMetadata(config)
        rootinfo = metadata.get_root_info("public")
        logging.info(f"MetadataTests.test_root_info: rootinfo for public: {rootinfo}")
        self.assertIsNotNone( rootinfo, msg=f"no root info for public!")
        self.assertEqual( rootinfo.name, "public", msg=f"rootinfo.name must be public, not {rootinfo.name}")
        self.assertIn("cdocs", rootinfo.accepts, msg=f"rootinfo must accept 'cdocs': {rootinfo.accepts}")
        self.assertIn("xml", rootinfo.formats, msg=f"rootinfo must use 'xml': {rootinfo.formats}")
        features = metadata.features.get("public")
        self.assertIsNotNone(features, msg=f"features of 'public' must not be None")
        #search,git,transform
        self.assertEqual( len(features), 4, msg=f"'public' must have 4 features, not {len(features)}")

        features = metadata.features.get("json")
        logging.info(f"MetadataTests.test_root_info: features of json: {features}")
        self.assertIsNotNone(features, msg=f"features of 'json' must not be None")
        #transform
        self.assertEqual( len(features), 1, msg=f"'json' must have 1 features, not {len(features)}")
        self.assertIn("transform", features, msg=f"'json' must have 'transform': {features}")



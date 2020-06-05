import abc
import os
import time
from bdocs.building_metadata import BuildingMetadata
from cdocs.contextual_docs import FilePath
from bdocs.rotater import Rotater

class SimpleRotater(Rotater):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def rotate(self, filepath:FilePath) -> FilePath:
        name = filepath[filepath.rindex(os.sep)+1:]
        dirname = filepath[0:filepath.rindex(os.sep)]
        return self._rotate(dirname, name)

    def _rotate(self, dirname, filename) -> FilePath:
        bakdir = os.path.join(dirname, "."+filename )
        if not os.path.exists( bakdir ):
            os.mkdir( bakdir )
        elif os.path.isfile( bakdir ):
            raise Exception(f"rotate: {bakdir} exists and is a file!")
        f = os.path.join(dirname, filename)
        t = os.path.join(dirname, "." + filename, str(int(time.time() * 1000)) + "-" + filename)
        os.rename(f, t)
        return t




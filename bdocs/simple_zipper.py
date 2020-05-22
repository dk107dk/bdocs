from  uuid import uuid4
import shutil
import logging
from cdocs.contextual_docs import FilePath
from bdocs.zipper import Zipper

class SimpleZipper(Zipper):

    def zip(self, filepath:FilePath) -> FilePath:
        auuid =  uuid4()
        auuid = str(auuid).replace('-', '_') + ".zip"
        print(f"zip.the uuid.zip is {auuid}")
        result = shutil.make_archive(auuid, 'zip', filepath)
        print(f"zip.the result is {result}")
        return result



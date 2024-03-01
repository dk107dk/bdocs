import os
import shutil
from typing import Optional
from cdocs.contextual_docs import FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.deleter import Deleter
import logging

class SimpleDeleter(Deleter):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def delete(self, filepath:FilePath, deleteDirIfFileNotFound:Optional[bool]=True) -> None:
        """ if deleteDirIfFileNotFound is true and if the filepath is not found
            we'll look for an extension (e.g. '.xml') and if there is one, remove it
            and try to delete a directory with that name.

            The reason to do this is that the user may give bdocs
            a directory docpath and bdocs may treat it as a file docpath.
            if the file is found that's fine because docpaths == files. but
            if the file isn't found we might be cleaning up a directory.

            in principle we could say that deleting a docpath means deleting
            the concept, a file, foremost, but also deleting any contextual
            information associated with the context at the same time, the
            directory. however, today that's not how it works.
        """
        try:
            if self.isdir(filepath):
                shutil.rmtree(filepath)
            else:
                os.remove(filepath)
        except FileNotFoundError as e:
            logging.debug(f'SimpleDeleter.delete: cannot delete: {e}')
            if deleteDirIfFileNotFound:
                i = filepath.find('.')
                if i > -1:
                    filepath = filepath[0:filepath.rindex('.')]
                    print(f"SimpleDeleter.delete: looking for a directory to delete at {filepath}")
                    self.delete(filepath, False)
            return None

    def delete_doc_tree(self, filepath:FilePath) -> None:
        self.delete(filepath)

    def isdir(self, filepath:FilePath) -> bool:
        return os.path.isdir(filepath)



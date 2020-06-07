from cdocs.contextual_docs import DocPath, FilePath
from bdocs.building_metadata import BuildingMetadata
from bdocs.mover import Mover
from bdocs.simple_mover import SimpleMover
from bdocs.git.git_writer import GitWriter
import logging

class GitMover(Mover):

    def __init__(self, metadata:BuildingMetadata, bdocs):
        self._metadata = metadata
        self._bdocs = bdocs

    def move_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        logging.debug(f"GitMover.move_doc: {fromdoc} -> {todoc}")
        simple_mover = SimpleMover(self._metadata, self._bdocs)
        logging.debug(f"GitMover.move_doc: moving using SimpleMover")
        simple_mover.move_doc(fromdoc, todoc)
        tofilepath = self._bdocs.pather.get_full_file_path(todoc)
        logging.debug(f"GitMover.move_doc: staging {tofilepath} and commiting with GitWriter")
        git_writer = GitWriter(self._metadata, self._bdocs)
        git_writer.stage_and_commit(tofilepath)
        logging.debug(f"GitMover.move_doc: {todoc} committed")
        fromfilepath = self._bdocs.pather.get_full_file_path(fromdoc)
        git_writer.stage_and_commit(fromfilepath)
        logging.debug(f"GitMover.move_doc: {fromdoc} done")

    def copy_doc(self, fromdoc:DocPath, todoc:DocPath) -> None:
        logging.debug(f"GitMover.copy_doc: {fromdoc} -> {todoc}")
        simple_mover = SimpleMover(self._metadata, self._bdocs)
        logging.debug(f"GitMover.copy_doc: copying using SimpleMover")
        simple_mover.copy_doc(fromdoc, todoc)
        tofilepath = self._bdocs.pather.get_full_file_path(todoc)
        logging.debug(f"GitMover.move_doc: staging {tofilepath} and commiting with GitWriter")
        git_writer = GitWriter(self._metadata, self._bdocs)
        git_writer.stage_and_commit(tofilepath)
        logging.debug(f"GitMover.move_doc: {todoc} done")



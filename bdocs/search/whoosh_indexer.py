import os
from cdocs.contextual_docs import JsonDict, DocPath, Doc, FilePath
from bdocs.indexer import Indexer
from bdocs.search.whoosh_index import WhooshIndex
from bdocs.search.index_doc import IndexDoc
from bdocs.building_metadata import BuildingMetadata
from typing import Optional
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
from whoosh.writing import AsyncWriter

class WhooshIndexer(WhooshIndex, Indexer):

    def __init__(self, metadata:BuildingMetadata, bdocs) -> None:
        super().__init__()
        self._metadata = metadata
        self._bdocs = bdocs
        self._index = self.get_index_root()
        self._check_index()

    def index_doc(self, path:DocPath, doc:Doc, metadata:Optional[IndexDoc]=None) -> None:
        if metadata is None:
            metadata = IndexDoc()
        ix = index.open_dir(self.get_index_root())
        writer = AsyncWriter(ix)
        writer.add_document(\
                            title=metadata.title,\
                            content=doc,\
                            path=path,\
                            root=self._bdocs.get_doc_root(),\
                            paths=metadata.paths,\
                            author=metadata.author,\
                            contributors=metadata.contributors,\
                            created=metadata.created,\
                            updated=metadata.updated\
                            )
        writer.commit()
        ix.close()

    def remove_doc(self, path:DocPath) -> None:
        ix = index.open_dir(self.get_index_root())
        writer = AsyncWriter(ix)
        writer.delete_by_term('path', path)
        writer.commit()



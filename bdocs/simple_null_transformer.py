import logging
from typing import Optional, Dict
from jinja2 import Template
from cdocs.contextual_docs import DocPath, FilePath, JsonDict
from cdocs.simple_config import SimpleConfig
from cdocs.transformer import Transformer
from cdocs.contextual_docs import DocPath
import inflect

class SimpleNullTransformer(Transformer):

    def __init__(self, cdocs): # can't type hint cdocs because circular
        self._cdocs = cdocs
        self._engine = inflect.engine()

    def transform(self, content:str, path:DocPath=None, \
                   tokens:Optional[Dict[str,str]]=None, transform_labels=True) -> str:
        logging.info("SimpleNullTransformer.transform: returning what you sent")
        return content



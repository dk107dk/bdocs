import abc
from cdocs.contextual_docs import JsonDict

class Walker(metaclass=abc.ABCMeta):

    # can't type hint Bdocs on the bdocs arg because it would
    # be a circular import ref.
    @abc.abstractmethod
    def get_doc_tree(self, bdocs) -> JsonDict:
        pass

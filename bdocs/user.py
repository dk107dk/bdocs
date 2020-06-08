import abc

class User(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def username(self) -> str:
        pass

    @abc.abstractmethod
    def password(self) -> str:
        pass


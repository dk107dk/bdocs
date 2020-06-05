import abc


class User(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def username(self) -> str:
        pass

    def password(self) -> str:
        pass


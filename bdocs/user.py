from typing import Protocol, runtime_checkable

@runtime_checkable
class NamedUser(Protocol):

    def name_of_user(self) -> str:
        pass



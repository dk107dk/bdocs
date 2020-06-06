from bdocs.user import User

class SimpleUser(User):

    def __init__(self, username):
        self._username = username
        self._password = None

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password


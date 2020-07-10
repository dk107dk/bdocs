from application.db.entities import Roles
from typing import List

class AdocsRoles(object):

    @classmethod
    def get_roles(cls) -> List[str]:
        return Roles.to_json()



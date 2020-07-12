from enum import Enum

class Roles(str, Enum):
    OWNER = "Owner"
    MEMBER = "Member"
    VIEWER = "Viewer"

    @classmethod
    def is_role(cls, arole):
        if not arole is Roles.OWNER and not arole is Roles.MEMBER and not arole is Roles.VIEWER:
            return False
        else:
            return True

    @classmethod
    def to_json(cls):
        j = "["
        j += json.dumps(cls.OWNER) + ","
        j += json.dumps(cls.MEMBER) + ","
        j += json.dumps(cls.VIEWER)
        j += "]"
        return j


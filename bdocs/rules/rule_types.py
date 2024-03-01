from enum import Enum

class RuleTypes(str, Enum):
    AVAILABLE_DURING = "available_during"
    UNAVAILABLE_DURING = "unavailable_during"
    UNAVAILABLE_AFTER = "unavailable_after"
    UNAVAILABLE_BEFORE = "unavailable_before"
    REPLACE_AFTER = "replace_after"
    REPLACE_UNTIL = "replace_until"
    RANDOM_AFTER = "random_after"
    RANDOM_UNTIL = "random_until"

    @classmethod
    def is_type(cls, atype):
        if not atype is RuleTypes.UNAVAILABLE_DURING and \
           not arole is RuleTypes.AVAILABLE_DURING and \
           not arole is RuleTypes.UNAVAILABLE_AFTER and \
           not arole is RuleTypes.UNAVAILABLE_BEFORE and \
           not arole is RuleTypes.REPLACE_AFTER and \
           not arole is RuleTypes.REPLACE_UNTIL and \
           not arole is RuleTypes.RANDOM_AFTER and \
           not arole is RuleTypes.RANDOM_UNTIL:
            return False
        else:
            return True

    @classmethod
    def get_type(cls, name):
        for t in cls:
            if t.value == name:
                return t
        return None

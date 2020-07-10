
from typing import Callable
from types import GeneratorType
import datetime


class UnexpectedResultException(Exception):
    pass

class DateUtils(object):

    @classmethod
    def fix_datetimes(cls, obs: list) -> None:
        print(f"DateUtils.fix_datetimes: obs: {obs}")
        if len(obs) == 0:
            return
        for i, _ in enumerate(obs):
            if isinstance(_,dict):
                cls.fix_datetime(_)
            elif isinstance(_, datetime.datetime):
                obs[i] = _.isoformat()
            else:
                pass

    @classmethod
    def fix_datetime(cls, o ) -> None:
        for k,v in o.items():
            if isinstance(v, datetime.datetime):
                o[k] = v.isoformat()
            elif isinstance(v,  datetime.date):
                o[k] = v.isoformat()

    def _wrap_fix_datetimes(self, func: Callable) -> Callable:
        def _a(self, *args, **kwargs):
            for _ in kwargs:
                print(f'a kwarg: {_} in {self} going into {func}')
            l = func(self, *args, **kwargs)
            ss = None
            # individual row comes as dict. multiple rows as list.
            if isinstance(l, dict):
                print(f"DateUtils._wrap_fix_datetime: dict: {l}")
                ss = [t for v,t in l.items()]
            elif isinstance(l, GeneratorType):
                print(f"DateUtils._wrap_fix_datetime.else: {type(l)}")
                ss = [t for t in l]
            elif isinstance(l, list): # does this ever happen?
                ss = [t for t in l]
            elif isinstance(l, str) :
                return l
            elif l == None:
                print("DateUtils._wrap_fix_datetimes: found None. returning [].")
                ss = []
            else:
                raise UnexpectedResultException(f"DateUtils._wrap_fix_datetimes: don't know what type l is: {type(l)}")
            DateUtils.fix_datetimes(ss)
            return ss
        return _a


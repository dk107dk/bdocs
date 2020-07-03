import logging
import datetime
from typing import Optional
from application.db.loader import Loader
from application.users.user import User

class SubscriptionException(Exception):
    pass

class Checker(object):

    @classmethod
    def incrementOrReject(cls, userid, field:str,
                               amount_to_increase:Optional[int]=None,
                               do_increment:Optional[bool]=True
                               ) -> bool:

        logging.info("Checker.incrementOrReject: {userid}, {field}, {amount_to_increase}, {do_increment}")
        loaded = Loader.load(User, userid)
        user = loaded.thing
        sub = user.subscription
        subt = user.subscription_tracker[0]
        result = Checker._check(sub,subt,field,amount_to_increase, do_increment)
        loaded.session.commit()
        logging.info("Checker.incrementOrReject: {userid}, {field}, {amount_to_increase}, {do_increment}: returning {result}")
        return result

    @classmethod
    def _check(cls, sub, subt, field:str, \
               amount_to_increase:Optional[int]=None, \
               do_increment:Optional[bool]=True) -> bool:
        if field == 'users':
            if sub.users <= subt.users:
                return False
            else:
                if do_increment:
                    subt.users += 1
        elif field == 'roots':
            if sub.roots <= subt.roots:
                return False
            else:
                if do_increment:
                    subt.roots += 1
        elif field == 'projects':
            if sub.projects <= subt.projects:
                return False
            else:
                if do_increment:
                    subt.projects += 1
        elif field == 'teams':
            if sub.teams <= subt.teams:
                return False
            else:
                if do_increment:
                    subt.teams += 1
        elif field == 'docs':
            if sub.docs <= subt.docs:
                return False
            else:
                if do_increment:
                    subt.docs += 1
        elif field == 'api_keys':
            if sub.api_keys <= subt.api_keys:
                return False
            else:
                if do_increment:
                    subt.api_keys += 1
        elif field == 'total_doc_bytes':
            if amount_to_increase is None or amount_to_increase < 0:
                raise SubscriptionException(f"amount_to_increase can not be \
{amount_to_increase} when checking total_doc_bytes")
            if sub.total_doc_bytes < subt.total_doc_bytes + amount_to_increase:
                return False
            else:
                if do_increment:
                    subt.total_doc_bytes += amount_to_increase
        elif field == 'api_calls':
            cls._check_api_call_period(sub, subt)
            if sub.api_keys < subt.api_calls:
                return False
            else:
                if do_increment:
                    subt.api_calls += 1
        return True

    @classmethod
    def _check_api_call_period(cls, sub, subt):
        val = datetime.date.today().month if  \
                sub.api_cycle == 'Monthly' else  \
                datetime.date.today().year
        logging.info(f"Checker._check_api_call_period: val: {val}")
        if subt.api_calls_current_period != val:
            logging.info(f"Checker._check_api_call_period: val != period: {subt.api_calls_current_period}")
            subt.api_calls = 0
            subt.api_calls_current_period = val



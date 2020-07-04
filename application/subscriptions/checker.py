import logging
import datetime
from typing import Optional,List
from application.db.loader import Loader
from application.db.database import Database
from application.db.entities import SubscriptionEntity, SubscriptionTrackingEntity

class SubscriptionException(Exception):
    pass

class Checker(object):

    @classmethod
    def decrement(cls, userid, field:str, decrease:Optional[int]=1):
        subid, subtid = cls._get_subs_ids(userid)

        subtloaded = Loader.load(SubscriptionTrackingEntity, subtid)
        subt = subtloaded.thing

        if field == "users":
            subt.users -= decrease
        elif field == "teams":
            subt.teams -= decrease
        elif field == "projects":
            subt.projects -= decrease
        elif field == "roots":
            subt.roots -= decrease
        elif field == "teams":
            subt.teams -= decrease
        elif field == 'docs':
            subt.docs -= decrease
        elif field == 'api_keys':
            subt.api_keys -= decrease
        elif field == 'total_doc_bytes':
            subt.total_doc_bytes -= decrease
        elif field == 'api_calls':
            subt.api_calls -= decrease

        subtloaded.session.commit()
        subtloaded.engine.dispose()


    @classmethod
    def incrementOrRejectFields(cls, userid, field:str,
                               amount_to_increase:Optional[int]=None,
                               do_increment:Optional[bool]=True
                               ) -> bool:
        results = cls.incrementOrReject(userid, [field],amount_to_increase, do_increment)
        return results[0]

    @classmethod
    def _get_subs_ids(cls, userid:str):
        result = None
        engine = Database().engine
        sql = f"select u.subscription_id, ust.subscription_tracking_id from \
                             user u, \
                             user_subscription_tracking ust \
                             where u.id='{userid}' and ust.user_id=u.id"
        logging.info(f"\n\n>>>>>>>>>>>>>>> sql: {sql}\n\n")
        with engine.connect() as c:
            rs = c.execute(sql)
            for row in rs:
                result = (row[0], row[1])
        engine.dispose()
        return result

    @classmethod
    def incrementOrReject(cls, userid, fields:List[str],
                               amount_to_increase:Optional[int]=None,
                               do_increment:Optional[bool]=True
                               ) -> bool:

        print(f">> Checker.incrementOrReject: {userid}, {fields}, {amount_to_increase}, {do_increment}")
        subid, subtid = cls._get_subs_ids(userid)

        subloaded = Loader.load(SubscriptionEntity, subid)
        sub = subloaded.thing

        subtloaded = Loader.load(SubscriptionTrackingEntity, subtid)
        subt = subtloaded.thing

        results = []
        for field in fields:
            result = Checker._check(sub,subt,field,amount_to_increase, do_increment)
            results.append(result)
        logging.info(f"Checker.incrementOrReject: {userid}, {field}, {amount_to_increase}, {do_increment}: returning {result}")

        subloaded.session.commit()
        subloaded.engine.dispose()

        subtloaded.session.commit()
        subtloaded.engine.dispose()
        return results

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



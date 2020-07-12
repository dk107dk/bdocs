import logging
from typing import Optional, Any
from application.db.loader import Loader
from application.db.database import Database

class AccountFinder(object):
    """ this class looks at the subscription tracking creator_id
        as the marker for the account owner id. currently only an
        account owner can create users, so any user's creator_id
        is the account owner. but this might change, so it's probably
        better to do it this way.
    """

    @classmethod
    def get_account_owner_id(cls, \
                userid:str) -> int:
        logging.info(f"AccountFinder.get_account_owner_id: userid: {userid}")
        aid = None
        engine = Database().engine
        sql = f"select subt.creator_id from user_subscription_tracking usubt, subscription_tracking subt where usubt.user_id='{userid}' and usubt.subscription_tracking_id=subt.id"
        logging.info(f"AccountFinder.get_account_owner_id: sql: {sql}\n\n")
        with engine.connect() as c:
            rs = c.execute(sql)
            for row in rs:
                aid = row[0]
        engine.dispose()
        logging.info(f"AccountFinder.get_account_owner_id: account owner id: {aid}")
        return aid

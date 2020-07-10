import logging
from typing import Optional, Any
from application.db.loader import Loader
from application.db.database import Database

class AccountFinder(object):

    @classmethod
    def get_account_owner_id(cls, \
                creator_id:str) -> str:
        logging.info(f"AccountFinder.get_account_owner_id: creator_id: {creator_id}")
        aid = None
        engine = Database().engine
        sql = f"select subt.creator_id from user_subscription_tracking usubt, subscription_tracking subt where usubt.user_id='{creator_id}' and usubt.subscription_tracking_id=subt.id"
        logging.info(f"AccountFinder.get_account_owner_id: creator_id: {creator_id}")
        logging.info(f"AccountFinder.get_account_owner_id: sql: {sql}\n\n")
        with engine.connect() as c:
            rs = c.execute(sql)
            for row in rs:
                aid = row[0]
        engine.dispose()
        logging.info(f"AccountFinder.get_account_owner_id: account owner id: {aid}")
        return aid

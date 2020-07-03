import logging
from typing import Optional, Any
from application.db.loader import Loader
from application.db.database import Database
from application.db.entities import SubscriptionEntity

class Finder(object):

    @classmethod
    def get_subscription_id_or_free_tier_id(cls, \
                creator_id:Optional[int]=None, \
                subscriptionid:Optional[int]=None) -> int:
        print(f"Finder.get_subscription_id_or_free_tier_id: creator_id: {creator_id}, subscriptionid: {subscriptionid}")
        if subscriptionid is None:
            if creator_id is None:
                loaded = Loader.load_by_name(SubscriptionEntity, "Free tier")
                print(f"Finder.get_subscription_id_or_free_tier_id: loaded.thing: {loaded.thing}")
                subscriptionid = loaded.thing.id
                loaded.session.close()
                loaded.engine.dispose()
            else:
                sid = None
                engine = Database().engine
                with engine.connect() as c:
                    rs = c.execute(f'select subscription_id from user where id={creator_id}')
                    for row in rs:
                        sid = row[0]
                engine.dispose()
                print(f"Finder.get_subscription_id_or_free_tier_id: sid: {sid}")
                subscriptionid = sid
        print(f"Finder.get_subscription_id_or_free_tier_id: subscriptionid: {subscriptionid}")
        return subscriptionid

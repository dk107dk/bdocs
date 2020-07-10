from application.db.entities import SubscriptionEntity, SubscriptionTrackingEntity
from typing import Dict, List

class AdocsSubscriptions(object):

    @classmethod
    def get_subscription(cls, id:int):
        return cls._get_thing(SubscriptionEntity,id)

    @classmethod
    def get_subscription_tracking(cls, id:int):
        return cls._get_thing(SubscriptionTrackingEntity,id)




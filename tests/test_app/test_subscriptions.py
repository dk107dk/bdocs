from application.db.database import Database
from application.db.entities import SubscriptionEntity, SubscriptionTrackingEntity
from application.db.standup import Standup, Shutdown
from application.subscriptions.checker import Checker
from application.subscriptions.subscription_finder import SubscriptionFinder
from application.subscriptions.account_finder import AccountFinder
from application.db.entities import Roles
from application.users.user import User
from bdocs.bdocs_config import BdocsConfig
import unittest
from sqlalchemy import inspect
from sqlalchemy.sql import text
from contextlib import closing
import datetime

class SubscriptionTests(unittest.TestCase):

    noise = BdocsConfig().get_with_default("testing", "SubscriptionTests_noise", "on") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get_with_default("testing", "SubscriptionTests", "on") == "off"

    def test_account_finder(self):
        self._print(f"SubscriptionTests.test_account_finder")
        if self._off(): return
        Shutdown()()
        Standup()()

        user = User(given_name='d',family_name='k', subscription_id=1)
        engine = Database().engine
        with closing(engine.session()) as session:
            user.create_me(session)
        engine.dispose()
        self._print(f">>>>>> SubscriptionTests.test_account_finder: user 1: {user}: user_id: {user.id}")

        user2 = User(given_name='a',family_name='c', creator_id=user.id)
        self._print(f">>>>>>>>> prepared user2: {user2}: {user2.creator_id}\n")
        engine = Database().engine
        with closing(engine.session()) as session:
            result = user2.create_me(session)
            session.commit()
            self._print(f">>>>>>>>> created user2: {result}: {user2}: id: {user2.id}: creator: {user2.creator_id}\n")
        engine.dispose()

        self._print(f"SubscriptionTests.test_account_finder: user 2: {user2}: {user2.id}")
        aid = AccountFinder.get_account_owner_id(user2.id)
        self.assertEqual(aid, user.id, msg=f'account owner id must be {user.id}, not {aid}')
        Shutdown()()

    def test_subscription_finder(self):
        self._print(f"SubscriptionTests.test_subscription_finder")
        if self._off(): return

        Shutdown()()
        Standup()()
        #
        # test: creator_id, subscriptionid, neither
        #
        user = User(given_name='d',family_name='k', subscription_id=1)
        engine = Database().engine
        with closing(engine.session()) as session:
            user.create_me(session)
        engine.dispose()
        sid = SubscriptionFinder.get_subscription_id_or_free_tier_id(creator_id=user.id)
        self.assertEqual(sid, 1, msg=f'for creator_id, subsciptionid must be 1, not {sid}')
        sid = SubscriptionFinder.get_subscription_id_or_free_tier_id(subscriptionid=1)
        self.assertEqual(sid, 1, msg=f'for subscriptionid, subsciptionid must be 1, not {sid}')
        sid = SubscriptionFinder.get_subscription_id_or_free_tier_id()
        self.assertEqual(sid, 1, msg=f'for None, subsciptionid must be 1, not {sid}')
        Shutdown()()

    def test_subscription_checker(self):
        self._print(f"SubscriptionTests.test_subscription_checker")
        if self._off(): return

        sub = SubscriptionEntity()
        subt = SubscriptionTrackingEntity()

        # users
        sub.users = 2
        subt.users = 1
        self.assertTrue(Checker._check(sub,subt, "users"), msg=f"users failed")
        self.assertEqual(subt.users, 2, msg=f"users failed")
        sub.users = 1
        subt.users = 1
        self.assertFalse(Checker._check(sub,subt, "users"), msg=f"users failed")

        # roots
        sub.roots = 2
        subt.roots = 1
        self.assertTrue(Checker._check(sub,subt, "roots"), msg=f"roots failed")
        self.assertEqual(subt.roots, 2, msg=f"roots failed")
        sub.roots = 1
        subt.roots = 1
        self.assertFalse(Checker._check(sub,subt, "roots"), msg=f"roots failed")

        # projects
        sub.projects = 2
        subt.projects = 1
        self.assertTrue(Checker._check(sub,subt, "projects"), msg=f"projects failed")
        self.assertEqual(subt.projects, 2, msg=f"projects failed")
        sub.projects = 1
        subt.projects = 1
        self.assertFalse(Checker._check(sub,subt, "projects"), msg=f"projects failed")

        # teams
        sub.teams = 2
        subt.teams = 1
        self.assertTrue(Checker._check(sub,subt, "teams"), msg=f"teams failed")
        self.assertEqual(subt.teams, 2, msg=f"teams failed")
        sub.teams = 1
        subt.teams = 1
        self.assertFalse(Checker._check(sub,subt, "teams"), msg=f"teams failed")

        # docs
        sub.docs = 2
        subt.docs = 1
        self.assertTrue(Checker._check(sub,subt, "docs"), msg=f"docs failed")
        self.assertEqual(subt.docs, 2, msg=f"docs failed")
        sub.docs = 1
        subt.docs = 1
        self.assertFalse(Checker._check(sub,subt, "docs"), msg=f"docs failed")

        # total_doc_bytes
        sub.total_doc_bytes = 20
        subt.total_doc_bytes = 10
        increase = 10
        self.assertTrue(Checker._check(sub,subt, "total_doc_bytes", increase), msg=f"total_doc_bytes failed")
        self.assertEqual(subt.total_doc_bytes, 20, msg=f"total_doc_bytes failed")
        sub.total_doc_bytes = 10
        subt.total_doc_bytes = 10
        self.assertFalse(Checker._check(sub,subt, "total_doc_bytes", increase), msg=f"total_doc_bytes failed")

        # api_keys
        sub.api_keys = 2
        subt.api_keys = 1
        self.assertTrue(Checker._check(sub,subt, "api_keys"), msg=f"api_keys failed")
        self.assertEqual(subt.api_keys, 2, msg=f"api_keys failed")
        sub.api_keys = 1
        subt.api_keys = 1
        self.assertFalse(Checker._check(sub,subt, "api_keys"), msg=f"api_keys failed")

        # api_calls
        sub.api_calls = 2
        sub.api_cycle = "Monthly"
        subt.api_calls = 1
        subt.api_calls_current_period = datetime.date.today().month -1
        self._print(f"SubscriptionTests.test_subscription_checker: current period 1: {subt.api_calls_current_period}")
        self.assertTrue(Checker._check(sub,subt, "api_calls"), msg=f"api_calls failed")
        self.assertEqual(subt.api_calls, 1, msg=f"api_calls failed")
        self._print(f"SubscriptionTests.test_subscription_checker: current period 2: {subt.api_calls_current_period}")
        self.assertTrue(Checker._check(sub,subt, "api_calls"), msg=f"api_calls failed")
        self.assertEqual(subt.api_calls, 2, msg=f"api_calls failed")
        sub.api_calls = 1
        subt.api_calls = 5
        self.assertFalse(Checker._check(sub,subt, "api_calls"), msg=f"api_calls failed")
        self.assertEqual(subt.api_calls, 5, msg=f"api_calls failed")






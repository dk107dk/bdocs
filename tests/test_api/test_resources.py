from application.app_config import AppConfig
from bdocs.bdocs_config import BdocsConfig
from adocs.resources import Resources
from adocs.adocs import Adocs
from application.users.user import User
from application.db.loader import Loader
from application.db.standup import Shutdown, Standup
import unittest
import logging

from application.roots.doc_root_management import DocRootManagement
from cdocs.cdocs import Cdocs

class ResourcesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setting up ResourcesTests")
        AppConfig.setTesting()

    noise = BdocsConfig().get("testing", "ResourcesTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "ResourcesTests", "on") == "off"

    logger = logging.getLogger('')
    def _debug(self):
        self.logger.setLevel(level=logging.DEBUG)
        self.logger.debug("SET THE LEVEL TO DEBUG")

    def test_get_resources(self):
        self._print(f"ResourcesTests.test_get_resources")
        if self._off(): return
        resources = Resources()
        rs = resources.get_resources()
        self.assertIsNotNone(rs, msg=f'must be some resources')
        self.assertNotEqual(len(rs), 0, msg=f'must be at least one resource')

    def test_get_users_by_creator(self):
        self._print(f"ResourcesTests.test_get_users_by_creator")
        if self._off(): return
        self._print("ResourcesTests.test_get_users_by_creator: setting up")
        Shutdown()()
        Standup()()
        Standup().create_test_entities()
        self._print("ResourcesTests.test_get_users_by_creator: doing test")
        adminid = Standup.get_admin_id()
        users = Adocs.get_users_created_by(adminid)
        self._print(">>>>>>>>>> ResourcesTests.test_get_users_by_creator: users: {users}")
        for user in users:
            self._print(f"ResourcesTests.test_get_users_by_creator:      user: {user}")
        # test changed because setup changed. we now have admin just create themselves.
        # the two users are created separately so that the first becomes account owner and
        # has team and project created. they then create the 2nd user.
        self.assertEqual(len(users), 1, msg=f'there must be 1 user, admin')

        users = Adocs.get_users_created_by(2)
        self._print(">>>>>>>>>> ResourcesTests.test_get_users_by_creator: users: {users}")
        for user in users:
            self._print(f"ResourcesTests.test_get_users_by_creator:      user: {user}")
        self.assertEqual(len(users), 2, msg=f'there must be 2 users')

        Shutdown()()

    def test_get_doc(self):
        self._print(f"ResourcesTests.test_get_doc")
        if self._off(): return
        #self._debug()
        self._print("ResourcesTests.test_get_doc: setting up")
        Shutdown()()
        Standup()()
        Standup().create_test_entities()
        self._print("ResourcesTests.test_get_doc: doing test")
        adminid = Standup.get_admin_id()
        doc = Adocs.get_doc_at_path(adminid, '/test_doc')
        self._print(f"ResourcesTests.test_get_doc: doc: {doc}")
        self.assertIsNotNone(doc, msg="doc cannot be None")
        found = doc.find("Hello") > -1
        self.assertEqual(found, True, msg=f"doc: {doc} must include 'Hello'")
        Shutdown()()


    def test_create_user(self):
        self._print(f"ResourcesTests.test_create_user")
        if self._off(): return
        #self._debug()
        self._print("ResourcesTests.test_create_user: setting up")
        Shutdown()()
        Standup()()
        Standup().create_test_entities()
        self._print("ResourcesTests.test_create_user: doing test")
        adminid = Standup.get_admin_id()

        userdata = {}
        userdata['given_name'] = 'fish'
        userdata['family_name'] = 'blue'
        userdata['user_name'] = 'fish@fish.com'
        userdata['creator_id'] = adminid
        userdata['subscription_id'] = None

        user = Adocs.create_user(1, userdata)
        print(f'ResourcesTests.test_create_user: created: {user}')
        self.assertIsNotNone(user, msg=f'user must not be None')
        self.assertEqual(user.get('given_name'), userdata.get('given_name'), msg=f'given name must be {userdata["given_name"]}')


        Shutdown()()






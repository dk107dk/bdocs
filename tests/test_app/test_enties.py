from application.db.database import Database
from application.db.loader import Loader, Loaded
from application.db.entities import Base, UserEntity, SubscriptionEntity
from application.users.user import User
from application.teams.team import Team
from application.projects.project import Project
from application.db.standup import Standup, Shutdown
from application.app_config import AppConfig
from application.db.entities import Roles
from bdocs.bdocs_config import BdocsConfig
import os
import shutil
import unittest
from contextlib import closing

class EntityTests(unittest.TestCase):

    noise = BdocsConfig().get("testing", "EntityTests_noise", "on") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "EntityTests", "on") == "off"

    def test_project_create_and_delete_dir(self):
        self._print(f"EntityTests.test_project_create_and_delete_dir")
        if self._off(): return

        Shutdown()()
        Standup()()

        cfg = AppConfig()

        uid = None
        user = None
        teams = None
        projects = None
        engine = Database().engine
        with closing(engine.session()) as session:
            user = User(given_name='David', family_name='K', user_name='d@k.com')
            user.create_me(session)
            session.commit()
            uid = user.id
            session.commit()
            teams = user.teams
            session.commit()
            projects = user.projects
        print(f'EntityTests.test_create_user_team_project_root: user: {user}: {user.subscription_id}')
        engine.dispose()

        print(f'EntityTests.test_project_create_and_delete_dir: user: {str(uid)}, team: {str(teams[0].id)}, project: {str(projects[0].id)}')
        root = cfg.get("ur", "root")
        path = root + os.sep + \
               str(uid)[0:1] + \
               os.sep + str(uid)[1:2] \
               + os.sep + str(uid) \
               + os.sep + str(teams[0].id) \
               + os.sep + str(projects[0].id) \
               + os.sep + "docs"\
               + os.sep + "default"
        print(f"EntityTests.test_project_create_and_delete_dir: path: {path}")

        rootexists = os.path.exists(path)
        self.assertEqual(True, rootexists, msg=f"root at {path} must exist")

        loaded = Loader.load(Project, projects[0].id)
        project = loaded.thing
        project.delete_project_dir()
        loaded.done()

        rootexists = os.path.exists(path)
        self.assertNotEqual(True, rootexists, msg=f"root at {path} must not exist")
        #
        # clean up even more
        #
        path = root + os.sep + str(uid)[0:1]
        shutil.rmtree(path)
        Shutdown()()

    def test_create_user_team_project_root(self):
        self._print(f"EntityTests.test_create_user_team_project_root")
        if self._off(): return

        Shutdown()()
        Standup()()

        print(f'EntityTests.test_create_user_team_project_root: stood up database')

        loaded = Loader.load_by_name(SubscriptionEntity, "Free tier")
        sub = loaded.thing
        subid = sub.id
        print(f">>> this is the sub entity: {sub.__dict__}")
        setattr(sub, 'values', sub.__dict__.copy() )

        self.assertIsNotNone(sub, msg=f"'Free tier' subscription can not be None")
        print(f"the subscription is: {sub}: {sub.id}")
        loaded.done()
        uid = None
        engine = Database().engine
        with closing(engine.session()) as session:
            user = User(given_name='David', family_name='K', \
                        user_name='d@k.com', subscription_id=subid)
            user.create_me(session)
            session.commit()
            uid = user.id
            session.commit()
        print(f'EntityTests.test_create_user_team_project_root: user: {user}')
        engine.dispose()
        #
        #
        #
        loaded = Loader.load(User, uid)
        auser = loaded.thing
        print("\n\n\n****************************\n")
        auser.id
        print(f" __dict 1: {auser.__dict__}")
        print(f" user: {auser}: {auser.id}")
        print(f" __dict 2: {auser.__dict__}")
        print(f" new dict: {auser.get_dict()}")
        print("****************************\n\n\n\n")


        self.assertIsNotNone(auser, msg=f"'David' user can not be None")

        projects = auser.projects
        self.assertIsNotNone(projects, msg=f"'David''s projects can not be None")
        self.assertEqual(1, len(projects), msg=f"'David''s projects must be 1 not {len(projects)}")

        team = projects[0].team
        self.assertIsNotNone(team, msg=f"'David''s project's team can not be None")

        #
        # check subscription stuff
        #
        asub = auser.subscription
        self.assertEqual(subid, asub.id, msg=f"'David''s subscription must be {subid}, not {asub}")
        asubt = auser.subscription_tracking
        loaded.session.commit()

        print(f"EntityTests.test_create_user_team_project_root: asubt: {asubt}")
        print(f"EntityTests.test_create_user_team_project_root: sub: {sub}: {sub.__dict__}")
        self.assertIsNotNone(asubt, msg=f"'David''s subscription_tracking must not be None")
        self.assertEqual( len (asubt), 1, msg=f"'David''s subscription_tracking must equal 1, not {len(asubt)}")
        asubt = asubt[0]
        self.assertEqual(asubt.users, 1, msg=f"'David''s subscription.users must equal the tracking .users, not {asubt.users}")
        self.assertEqual(asubt.teams, 1, msg=f"'David''s sub tracking.teams must be 1, not {asubt.teams}")
        self.assertEqual(asubt.projects, 1, msg=f"'David''s sub tracking.projects must be 1, not {asubt.projects}")
        self.assertEqual(asubt.roots, 1, msg=f"'David''s sub tracking.roots must be 1, not {asubt.roots}")
        #
        # test update. set the value and commit. then repull the object and check.
        #
        auser.given_name = 'fish'
        loaded.session.commit()
        loaded.done()
        loaded = Loader.load(User, uid)
        auser = loaded.thing
        self.assertEqual(auser.given_name, 'fish', msg=f"'David' user must now have name 'fish', not {auser.given_name}")
        loaded.done()
        #
        # create team
        #
        loaded = Loader.load(User, uid)
        session = loaded.session
        auser = loaded.thing
        newteam = Team( name="Fish Team",  )
        auser.create_a_team(newteam, loaded.session )
        session.commit()

        #
        # create another user
        #
        seconduser = User(given_name='Bats', family_name='Frogs', user_name='fish@bats.frog')
        print(f'EntityTests.test_create_user_team_project_root: seconduser: {seconduser}')
        seconduser.create_me(session, auser.id, auser.subscription_id)
        session.commit()
        seconduser.add_me_to_team(newteam.id, Roles.MEMBER, session)
        session.commit()
        seconduserid = seconduser.id
        session.commit()
        loaded.done()

        loaded = Loader.load(User, seconduserid)
        auser = loaded.thing
        teams = auser.teams
        self.assertIsNotNone(teams, msg=f"teams must not be None")
        self.assertEqual(len(teams), 1, msg=f"{auser.given_name} ({auser.id}) must have 1 teams, not {len(teams)}")
        loaded.done()

        Shutdown()()




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

    noise = BdocsConfig().get_with_default("testing", "EntityTests_noise", "on") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get_with_default("testing", "EntityTests", "on") == "off"

    def test_project_create_and_delete_dir(self):
        self._print(f"EntityTests.test_project_create_and_delete_dir")
        if self._off(): return

        cfg = AppConfig()
        userid = 12345
        teamid = 6789
        project = Project(name='My project', team_id=teamid, creator_id=userid)
        project.id = 101112
        project.creator_id = userid
        print(f'EntityTests.test_project_create_and_delete_dir: user: {str(userid)}, team: {str(teamid)}, project: {str(project.id)}')
        project.create_my_root( userid, teamid )
        self._print(f"EntityTests.test_project_create_and_delete_dir: created dir")
        root = cfg.get("ur", "root")
        path = root + os.sep + \
               str(userid)[0:1] + \
               os.sep + str(userid)[1:2] \
               + os.sep + str(userid) \
               + os.sep + str(teamid) \
               + os.sep + str(project.id) \
               + os.sep + "docs"\
               + os.sep + "default"
        print(f"EntityTests.test_project_create_and_delete_dir: path: {path}")

        rootexists = os.path.exists(path)
        self.assertEqual(True, rootexists, msg=f"root at {path} must exist")

        project.delete_project_dir()

        rootexists = os.path.exists(path)
        self.assertNotEqual(True, rootexists, msg=f"root at {path} must not exist")

        path = root + os.sep + str(userid)[0:1]
        shutil.rmtree(path)

    def test_create_user_team_project_root(self):
        self._print(f"EntityTests.test_create_user_team_project_root")
        if self._off(): return

        Shutdown()()
        Standup()()
        print(f'EntityTests.test_create_user_team_project_root: stood up database')

        loaded = Loader.load_by_name(SubscriptionEntity, "Free tier")
        sub = loaded.thing
        self.assertIsNotNone(sub, msg=f"'Free tier' subscription can not be None")
        print(f"the subscription is: {sub}: {sub.id}")

        engine = Database().engine
        with closing(engine.session()) as session:
            user = User(given_name='David', family_name='K', \
                        user_name='d@k.com', subscription_id=sub.id)
            user.create_me(session)
        print(f'EntityTests.test_create_user_team_project_root: user: {user}: {user.subscription_id}')
        engine.dispose()
        #
        #
        #
        loaded = Loader.load(User, user.id)
        auser = loaded.thing
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
        self.assertEqual(sub.id, asub.id, msg=f"'David''s subscription must be {sub.id}, not {asub}")
        asubt = auser.subscription_tracking
        print(f"EntityTests.test_create_user_team_project_root: asubt: {asubt}")
        print(f"EntityTests.test_create_user_team_project_root: sub: {sub}: {sub.users}")
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
        loaded = Loader.load(User, user.id)
        auser = loaded.thing
        self.assertEqual(auser.given_name, 'fish', msg=f"'David' user must now have name 'fish', not {auser.given_name}")
        loaded.done()
        #
        # create team
        #
        loaded = Loader.load(User, user.id)
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
        seconduser.add_me_to_team(newteam, Roles.MEMBER, session)
        seconduserid = seconduser.id
        loaded.done()

        loaded = Loader.load(User, seconduserid)
        auser = loaded.thing
        teams = auser.teams
        self.assertIsNotNone(teams, msg=f"teams must not be None")
        self.assertEqual(len(teams), 2, msg=f"{auser} must have 2 teams, not {len(teams)}")
        loaded.done()

        loaded = Loader.load(User, seconduserid)
        seconduser = loaded.thing
        teams = seconduser.teams
        self.assertIsNotNone(teams, msg=f"teams must not be None")
        self.assertEqual(len(teams), 2, msg=f"{auser} must have 2 teams, not {len(teams)}")
        loaded.done()
        """
        """
        #Shutdown()()




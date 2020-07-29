from application.db.database import Database
from application.db.loader import Loader, Loaded
from application.db.entities import Base, UserEntity, SubscriptionEntity
from application.users.user import User
from application.teams.team import Team
from application.projects.project import Project
from application.db.standup import Standup, Shutdown
from application.app_config import AppConfig
from application.db.roles import Roles
from bdocs.bdocs_config import BdocsConfig
import os
import shutil
import unittest
from contextlib import closing

class EntityTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setting up EntityTests")
        AppConfig.setTesting()


    noise = BdocsConfig().get("testing", "EntityTests_noise", "on") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "EntityTests", "on") == "off"


    def test_owner_member(self):
        self._print(f"EntityTests.test_owner_member")
        if self._off(): return

        Shutdown()()
        Standup()()

        self._print("EntityTests.test_owner_member: starting")

        engine = Database().engine
        with closing(engine.session()) as session:
            # create user, their team, its project
            user = User(given_name='D', family_name='K', user_name='d@k.com')
            user.create_me(session)
            session.commit()
            uid = user.id
            session.commit()
            teams = user.teams
            session.commit()
            projects = user.projects
            self.assertIsNotNone(projects, msg=f'user must have projects')
            self.assertEqual(len(projects), 1, msg=f'user must have 1 projects')
            project = projects[0]

            # check how many users in project?
            users = project.count_users(session)
            self.assertEqual(1, users, msg=f"there must be 1 user in project {project.id}")

            # create 2nd user
            user2 = User(given_name='C', family_name='B', user_name='c@b.com', creator_id=user.id)
            user2.create_me(session)
            session.commit()

            # verify that 2nd user is not in project and can't update or delete it
            self.assertEqual(project.is_user_in(user2.id,session), False, msg=f'user {user2.id} is not in project {project.id}')
            can = project.can_update_or_delete(user2.id, session)
            self._print(f"EntityTests.test_owner_member: can: {can}")
            self.assertEqual(can, False, msg=f'user {user2.id} must not be able to update project {project.id}')

            # add 2nd user to project
            project.make_member(user2.id, session)
            self.assertEqual(project.is_user_in(user2.id,session), True, msg=f'user {user2.id} is in project {project.id}')
            self.assertEqual(can, False, msg=f'user {user2.id} must still not be able to update project {project.id} even as a member')
            ids = project.get_member_ids(session)
            self.assertEqual(len(ids), 1, msg=f"there must be 1 members in project {project.id}")

            # check that both users are in project
            users = project.count_users(session)
            self.assertEqual(2, users, msg=f"there must be 2 user in project {project.id}")
            idroles = project.get_id_roles(session)
            self.assertEqual(len(idroles), 2, msg=f"there must be 2 members in project {project.id} so 2 id roles")

            # check the ids have the right roles
            self._print(f"EntityTests.test_owner_member: idroles: {idroles}")
            foundo = False
            foundm = False
            for _ in idroles:
                if _[0] == user.id and _[1] == "Owner":
                    foundo = True
                if _[0] == user2.id and _[1] == "Member":
                    foundm = True
            self.assertEqual(foundo, True, msg=f"didn't find {user.id} with 'Owner'")
            self.assertEqual(foundm, True, msg=f"didn't find {user2.id} with 'Member'")

            # promote 2nd user to be project owner
            project.make_owner(user2.id, session)
            self.assertEqual(project.is_user_in(user2.id,session), True, msg=f'user {user2.id} is still in project {project.id}')
            can = project.can_update_or_delete(user2.id, session)
            self.assertEqual(can, True, msg=f'user {user2.id} must be able to update project {project.id} as owner')
            ids = project.get_member_ids(session)
            self.assertEqual(len(ids), 0, msg=f"there must be 0 members in project {project.id}")

            # make sure project has 2 owners
            ids = project.get_owner_ids(session)
            self.assertEqual(len(ids), 2, msg=f"there must be 2 owners in project {project.id}")

            # make sure 2nd user can update or delete
            can = project.can_update_or_delete(user2.id, session)
            self.assertEqual(can, True, msg=f'user {user2.id} must be able to update project {project.id}')

            # remove 2nd user and check owners, count
            project.remove_user_with_role(user2.id, session)
            ids = project.get_owner_ids(session)
            self.assertEqual(len(ids), 1, msg=f"there must be 1 owners in project {project.id}")
            users = project.count_users(session)
            self.assertEqual(1, users, msg=f"there must be 1 user in project {project.id}")

        engine.dispose()
        Shutdown()()





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
        self._print(f'EntityTests.test_create_user_team_project_root: user: {user}: {user.subscription_id}')
        engine.dispose()

        self._print(f'EntityTests.test_project_create_and_delete_dir: user: {str(uid)}, team: {str(teams[0].id)}, project: {str(projects[0].id)}')
        root = cfg.get_ur_root_path()
        path = root + os.sep + \
               str(uid)[0:1] + \
               os.sep + ( str(uid) if len(str(uid)) == 1 else str(uid)[1:2] ) \
               + os.sep + str(uid) \
               + os.sep + str(teams[0].id) \
               + os.sep + str(projects[0].id) \
               + os.sep + "docs"\
               + os.sep + "my_project"
        self._print(f"EntityTests.test_project_create_and_delete_dir: path: {path}")

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

        self._print(f'EntityTests.test_create_user_team_project_root: stood up database')

        loaded = Loader.load_by_name(SubscriptionEntity, "Free tier")
        sub = loaded.thing
        subid = sub.id
        self._print(f">>> this is the sub entity: {sub.__dict__}")
        setattr(sub, 'values', sub.__dict__.copy() )

        self.assertIsNotNone(sub, msg=f"'Free tier' subscription can not be None")
        self._print(f"the subscription is: {sub}: {sub.id}")
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
        self._print(f'EntityTests.test_create_user_team_project_root: user: {user}')
        engine.dispose()
        #
        #
        #
        loaded = Loader.load(User, uid)
        auser = loaded.thing
        self._print("\n\n\n****************************\n")
        auser.id
        self._print(f" __dict 1: {auser.__dict__}")
        self._print(f" user: {auser}: {auser.id}")
        self._print(f" __dict 2: {auser.__dict__}")
        self._print(f" new dict: {auser.get_dict()}")
        self._print("****************************\n\n\n\n")


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

        self._print(f"EntityTests.test_create_user_team_project_root: asubt: {asubt}")
        self._print(f"EntityTests.test_create_user_team_project_root: sub: {sub}: {sub.__dict__}")
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
        self._print(f'EntityTests.test_create_user_team_project_root: seconduser: {seconduser}')
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




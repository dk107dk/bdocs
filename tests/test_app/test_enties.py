from application.db.database import Database
from application.db.entities import Base, UserEntity
from application.users.user import User
from application.teams.team import Team
from application.projects.project import Project
from application.db.standup import Standup, Shutdown
from application.app_config import AppConfig
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

        return

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

        engine = Database().engine
        with closing(engine.session()) as session:
            user = User(given_name='David', family_name='Kershaw', user_name='dkershaw@post.harvard.edu')
            print(f'EntityTests.test_create_user_team_project_root: user: {user}')
            user.create_me(session)

            auser = session.query(User).filter_by(given_name='David').first()
            session.commit()
            self.assertIsNotNone(auser, msg=f"'David' user can not be None")

            projects = auser.projects
            self.assertIsNotNone(projects, msg=f"'David''s projects can not be None")
            self.assertEqual(1, len(projects), msg=f"'David''s projects must be 1 not {len(projects)}")

            team = projects[0].team
            self.assertIsNotNone(team, msg=f"'David''s project's team can not be None")
        engine.dispose()

        Shutdown()()


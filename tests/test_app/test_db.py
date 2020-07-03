from application.db.database import Database
from application.db.entities import UserEntity, TeamEntity, ProjectEntity, RoleEntity, Base
from application.db.standup import Standup, Shutdown
from application.app_config import AppConfig
from application.db.entities import Roles
from bdocs.bdocs_config import BdocsConfig
import unittest
from sqlalchemy import inspect
from sqlalchemy.sql import text
from contextlib import closing

class DatabaseTests(unittest.TestCase):

    noise = BdocsConfig().get_with_default("testing", "DatabaseTests_noise", "on") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get_with_default("testing", "DatabaseTests", "on") == "off"

    def test_connection(self):
        self._print(f"DatabaseTests.test_connection")
        if self._off(): return
        engine = Database().engine
        print(f'DatabaseTests.test_connection: engine: {engine}, session: {session}')
        with engine.connect() as connection:
            print(f"DatabaseTests.test_connection: connection: {connection}")
        engine.dispose()

    def test_standup(self):
        self._print(f"DatabaseTests.test_standup")
        if self._off(): return

        self._print(f"DatabaseTests.test_standup: standing up")
        Standup()()
        self._print(f"DatabaseTests.test_standup: stood up")

        engine = Database().engine
        inspector = inspect(engine)
        columns = inspector.get_columns('user')
        self._print(f"DatabaseTests.test_standup: columns: {columns}")
        self.assertIsNotNone( columns, msg="user columns cannot be None")
        self.assertNotEqual( 0, len(columns), msg=f"user table must have columns")
        rolecount = 0
        with engine.connect() as c:
            rs = c.execute('select * from role')
            self.assertIsNotNone( rs, msg="results cannot be None")
            for row in rs:
                rolecount += 1
        self.assertEqual( 3, rolecount, msg=f"roles table must have 3 roles")
        engine.dispose()

        self._print(f"DatabaseTests.test_standup: shutting down")
        Shutdown()()
        self._print(f"DatabaseTests.test_standup: shut down")


    def test_user(self):
        self._print(f"DatabaseTests.test_user")
        if self._off(): return

        user = UserEntity(given_name='David', family_name='Kershaw', user_name='dkershaw@post.harvard.edu')
        print(f'DatabaseTests.test_user: user: {user}')

        engine = Database().engine
        with closing(engine.session()) as session:
            print(f'DatabaseTests.test_user: engine: {engine}, session: {session}')

            print(f'DatabaseTests.test_user: dropping all tables')
            Base.metadata.drop_all(engine)

            print(f'DatabaseTests.test_user: creating all tables')
            Base.metadata.create_all(engine)
            print(f'DatabaseTests.test_user: created user table')
            session.add(user)
            print(f'DatabaseTests.test_user: added user')
            session.commit()
            print(f'DatabaseTests.test_user: commited user')
            auser = session.query(UserEntity).filter_by(given_name='David').first()
            print(f"DatabaseTests.test_user: queried for auser: {auser}")
            self.assertIsNotNone(auser, msg=f'user must not be None')
            session.commit()

        Base.metadata.drop_all(engine)
        engine.dispose()

    def test_all(self):
        self._print(f"DatabaseTests.test_all")
        if self._off(): return

        Shutdown()()
        Standup()()

        engine = Database().engine
        with closing(engine.session()) as session:
            owner = session.query(RoleEntity).filter_by(id=Roles.OWNER).first()
            member = session.query(RoleEntity).filter_by(id=Roles.MEMBER).first()
            print(f"DatabaseTests.test_all: found roles: {[owner, member]}")

            david = UserEntity(given_name='David', family_name='Kershaw', user_name='dkershaw@post.harvard.edu')
            print(f'DatabaseTests.test_all: user: {david}')
            session.add(david)
            john = UserEntity(given_name='John', family_name='Doe', user_name='doe@john.com')
            print(f'DatabaseTests.test_all: user: {john}')
            session.add(john)
            session.commit()
            print(f'DatabaseTests.test_all: added user')

            team = TeamEntity(name='my team', creator_id=david.id )
            print(f'DatabaseTests.test_all: team: {team}')
            session.add(team)
            session.commit()
            with engine.connect() as c:
                stmt = text(f"insert into user_team_role(user_id, team_id, role_id)\
                          values({david.id}, {team.id}, '{Roles.OWNER.value}')")
                c.execute(stmt)
                stmt = text(f"insert into user_team_role(user_id, team_id, role_id)\
                          values({john.id}, {team.id}, '{Roles.MEMBER.value}')")
                c.execute(stmt)
            session.commit()

            print(f'DatabaseTests.test_all: added team')

            project = ProjectEntity(name='my project', team_id=team.id, creator_id=david.id)
            print(f'DatabaseTests.test_all: project: {project}')
            session.add(project)
            session.commit()

            with engine.connect() as c:
                stmt = text(f"insert into user_project_role(user_id, project_id, role_id)\
                          values({david.id}, {project.id}, '{Roles.OWNER.value}')")
                c.execute(stmt)
                stmt = text(f"insert into user_project_role(user_id, project_id, role_id)\
                          values({john.id}, {project.id}, '{Roles.MEMBER.value}')")
                c.execute(stmt)
            print(f'DatabaseTests.test_all: added project')
            print("\n\n\n")

            # ------------------
            # now we check
            # ------------------

            aproject = session.query(ProjectEntity).filter_by(name='my project').first()
            print(f"DatabaseTests.test_all: my project: {aproject}: {aproject.name}\n")
            self.assertIsNotNone(aproject, msg=f"'my project' can not be None")

            ateam = aproject.team
            print(f"DatabaseTests.test_all: project has a team: {ateam}: {ateam.name}\n")
            self.assertIsNotNone(ateam, msg=f"'my project' must have a team")

            users = ateam.users
            print(f"DatabaseTests.test_all: team has users: {users}\n")
            self.assertIsNotNone(users, msg=f"'my project''s team must have users")
            self.assertEqual( len(users), 2, msg=f"'my project''s team must have 2 users, not {users}")

            teams = david.teams
            print(f"DatabaseTests.test_all: david has teams: {teams}\n")
            self.assertIsNotNone(teams, msg=f"david must have teams")
            self.assertEqual( len(teams), 1, msg=f"david must have 1 team, not {teams}")

            projects = david.projects
            print(f"DatabaseTests.test_all: david has projects: {projects}\n")
            self.assertIsNotNone(projects, msg=f"david must have projects")
            self.assertEqual( len(projects), 1, msg=f"david must have 1 project, not {projects}")

            projects = ateam.projects
            print(f"DatabaseTests.test_all: ateam has projects: {projects}\n")
            self.assertIsNotNone(users, msg=f"'my project''s team must have projects")
            self.assertEqual( len(projects), 1, msg=f"'my project''s team must have 1 project, not {projects}")

            session.commit()

        Shutdown()()



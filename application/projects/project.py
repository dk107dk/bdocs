import logging
from typing import Optional,Dict,Any
from application.db.entities import ProjectEntity, RoleEntity, UserEntity
from application.db.loader import Loader
from application.roots.doc_root_management import DocRootManagement
from application.roots.paths_finder import PathsFinder
from application.db.entities import Roles
from sqlalchemy.sql import text
import shutil

class Project(ProjectEntity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_me(self, theowner, theteamid, session): #cannot hint User
        """
        session must be an open session that can be used
        to create the new project's role associations.
        """
        session.add(self)
        session.commit()
        owner = session.query(RoleEntity).filter_by(name='Owner').first()
        with session.get_bind().engine.connect() as c:
            stmt = text(f"insert into user_project_role(user_id, project_id, role_id)\
                  values({theowner.id}, {self.id}, '{Roles.OWNER.value}')")
            c.execute(stmt)
        theowner.subscription_tracking[0].projects += 1
        session.commit()
        self.create_my_root(theowner.id, theteamid, session)

    def create_my_root(self, theownerid, theteam, session):
        mgmt = DocRootManagement()
        mgmt.create_project(theownerid, theteam, self.id)

        loaded = Loader.load(UserEntity, theownerid)
        theowner = loaded.thing
        theowner.subscription_tracking[0].roots += 1
        loaded.session.commit()


    def delete_project_dir(self):
        print(f"Project.delete_project_dir")
        finder = PathsFinder()
        accountid = self.creator_id
        teamid = self.team_id
        if teamid is None:
            raise Exception(f"Project.delete_project_dir: cannot delete {self.id} dir if project doesn't know its team id")
        projectid = self.id
        if projectid is None:
            raise Exception(f"Project.delete_project_dir: cannot delete {self.id} dir if project doesn't know its id")
        path = finder.get_project_path(accountid, teamid, projectid)
        print(f"Project.delete_project_dir: path: {path}")
        shutil.rmtree(path)



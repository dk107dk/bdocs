import logging
from typing import Optional,Dict,Any
from application.db.entities import ProjectEntity, RoleEntity
from application.roots.doc_root_management import DocRootManagement
from application.roots.paths_finder import PathsFinder
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
                  values({theowner.id}, {self.id}, {owner.id})")
            c.execute(stmt)
        self.create_my_root(theowner.id, theteamid)

    def create_my_root(self, theownerid, theteam):
        mgmt = DocRootManagement()
        mgmt.create_project(theownerid, theteam, self.id)

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



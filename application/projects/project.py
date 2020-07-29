import logging
from typing import Optional,Dict,Any
from application.db.entities import ProjectEntity, RoleEntity, UserEntity
from application.db.loader import Loader
from application.roots.doc_root_management import DocRootManagement
from application.subscriptions.checker import Checker
from application.subscriptions.account_finder import AccountFinder
from application.roots.paths_finder import PathsFinder
from application.db.roles import Roles
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
        ok = Checker.incrementOrReject(theowner.id, "projects")
        if ok:
            session.add(self)
            session.commit()
            owner = session.query(RoleEntity).filter_by(name='Owner').first()
            with session.get_bind().engine.connect() as c:
                stmt = text(f"insert into user_project_role(user_id, project_id, role_id)\
                      values({theowner.id}, {self.id}, '{Roles.OWNER.value}')")
                c.execute(stmt)
            theowner.subscription_tracking[0].projects += 1
            session.commit()
            self.create_my_root(theowner.id, theteamid )
            return True
        else:
            return False

    def create_my_root(self, theownerid, theteam ) -> bool:
        ok = Checker.incrementOrReject(theownerid, "roots")
        if ok:
            print("Project.create_my_root: starting")
            self._create_my_root(theownerid, theteam)
            loaded = Loader.load(UserEntity, theownerid)
            theowner = loaded.thing
            theowner.subscription_tracking[0].roots += 1
            loaded.session.commit()
            loaded.done()
        else:
            print("Project.create_my_root: cannot create root because subscription full")
            return False

    def _create_my_root(self, theownerid, theteam) -> bool :
        mgmt = DocRootManagement()
        mgmt.create_project(theownerid, theteam, self.id)
        return True

    def get_my_config(self):
        accountid = AccountFinder.get_account_owner_id(self.creator_id)
        teamid = self.team.id
        projectid = self.id
        mgmt = DocRootManagement()
        cfg = mgmt.get_config_of(accountid, teamid, projectid)
        return cfg

    def delete_project_dir(self):
        print(f"Project.delete_project_dir")
        """ need BdocsConfig for this project so we know how many
            roots to release in subscription tracking """
        numroots = len( self.get_my_config().get_items("docs") )
        accountid = AccountFinder.get_account_owner_id(self.creator_id)
        teamid = self.team_id
        if teamid is None:
            raise Exception(f"Project.delete_project_dir: cannot delete {self.id} dir if project doesn't know its team id")
        projectid = self.id
        if projectid is None:
            raise Exception(f"Project.delete_project_dir: cannot delete {self.id} dir if project doesn't know its id")
        path = PathsFinder().get_project_path(accountid, teamid, projectid)
        print(f"Project.delete_project_dir: path: {path}")
        shutil.rmtree(path)
        if numroots > 0:
            Checker.decrement(self.id, "roots", numroots)



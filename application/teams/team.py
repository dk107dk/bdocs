import logging
from typing import Optional,Dict,Any
from application.db.entities import TeamEntity, RoleEntity
from application.projects.project import Project
from sqlalchemy.sql import text
from application.db.entities import Roles

class Team(TeamEntity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_me(self, theowner, session):  # cannot hint User
        """
        session must be an open session that can be used
        to create the new team's project and role associations.
        """
        session.add(self)
        session.commit()
        owner = session.query(RoleEntity).filter_by(name='Owner').first()
        with session.get_bind().engine.connect() as c:
            stmt = text(f"insert into user_team_role(user_id, team_id, role_id)\
                      values({theowner.id}, {self.id}, '{Roles.OWNER.value}')")
            c.execute(stmt)
        session.commit()
        theowner.subscription_tracking[0].teams += 1
        session.commit()
        self.create_my_project(theowner, session)

    def create_my_project(self, theowner, session):  # cannot hint User
        project = Project(name='My project', team_id=self.id, creator_id=theowner.id)
        project.create_me(theowner, self.id, session)



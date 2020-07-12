import logging
from typing import Optional,Dict,Any
from application.db.entities import TeamEntity, RoleEntity
from application.projects.project import Project
from application.subscriptions.account_finder import AccountFinder
from sqlalchemy.sql import text
from application.db.roles import Roles
from application.subscriptions.checker import Checker

class Team(TeamEntity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_me(self, theowner, session) -> bool:  # cannot hint User
        # check if we're acting on behalf of the account owner
        aid = AccountFinder.get_account_owner_id(theowner.id)
        if not theowner.id == aid :
            logging.warning(f"Team.create_me: cannot create team: the new owner: {theowner.id} is not the account holder: {aid}")
            return False
        # check the subscription
        ok = Checker.incrementOrReject(theowner.id, "teams")
        if ok:
            self.creator_id = theowner.id
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
            return True
        else:
            return False

    def create_my_project(self, theowner, session):
        project = Project(name='My project', team_id=self.id, creator_id=theowner.id)
        project.create_me(theowner, self.id, session)




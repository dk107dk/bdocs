import logging
from typing import Optional,Dict,Any
from bdocs.simple_user import SimpleUser
from application.db.entities import UserEntity
from application.teams.team import Team

class User(UserEntity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_me(self, session):
        """
        session must be an open session that can be used
        to create the new user's team, project and role associations.
        """
        session.add(self)
        session.commit()
        self.create_my_team(session)

    def create_my_team(self,session):
        team = Team(name='My team', creator_id=self.id)
        team.create_me(self, session)


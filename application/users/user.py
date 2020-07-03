import logging
from typing import Optional #,Dict,Any
from bdocs.simple_user import SimpleUser
from application.db.entities import UserEntity, SubscriptionTrackingEntity
from application.db.database import Database
from application.teams.team import Team
from application.subscriptions.finder import Finder
from application.db.entities import Roles
from contextlib import closing
from sqlalchemy.sql import text

class User(UserEntity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_me(self, session, \
            creatorid:Optional[str]=None, \
            subscriptionid:Optional[int]=None) -> bool:
        """
        session must be an open session that can be used
        to create the new user's team, project and role associations.
        """
        self.creator_id = creatorid
        if self.subscription_id is None:
            self.subscription_id = Finder.get_subscription_id_or_free_tier_id(creatorid, subscriptionid)
        """ if creatorid is None we are creating an account owner """
        if creatorid is None:
            session.add(self)
            session.commit()
            self.creator_id = self.id
            sub = SubscriptionTrackingEntity(creator_id=self.id, users=1)
            session.add(sub)
            session.commit()
            self.subscription_tracking = [sub]
            session.commit()
            self.create_my_team(session)
            return True
        else:
            """ we are creating a regular user. they need to have
                the same subscription tracking as the account owner """
            ok = Checker.incrementOrReject(creatorid, "users")
            if ok:
                sub = session.query(SubscriptionTrackingEntity).filter_by(creator_id=self.creator_id).first()
                self.subscription_tracking = [sub]
                session.commit()
                sub.users = sub.users + 1
                session.commit()
            else:
                return False


    def create_my_team(self,session) -> None:
        team = Team(name='My team', creator_id=self.id)
        team.create_me(self, session)

    def create_a_team(self, team:Team, session) -> None:
        team.creator_id = self.id
        team.create_me(self, session)

    def add_me_to_team(self, team:Team, role:Roles, session) -> None:
        if not Roles.is_role(role):
            raise Exception(f"{role} is not a role")
        engine = Database().engine
        with session.get_bind().engine.connect() as c:
            stmt = text(f"insert into user_team_role(user_id, team_id, role_id)\
                      values({self.id}, {team.id}, '{role.value}')")
            c.execute(stmt)


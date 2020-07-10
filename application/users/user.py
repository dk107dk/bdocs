import logging
from typing import Optional #,Dict,Any
from bdocs.simple_user import SimpleUser
from application.db.entities import UserEntity, SubscriptionTrackingEntity
from application.db.database import Database
from application.teams.team import Team
from application.subscriptions.subscription_finder import SubscriptionFinder
from application.subscriptions.checker import Checker, SubscriptionException
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
        print(f"User.create_me: creating user: {self}: cid: {self.creator_id}")
        if creatorid is not None and self.creator_id is None:
            print(f"User.create_me: setting my creator_id to the passed in creatorid: {creatorid}")
            self.creator_id = creatorid
        elif self.creator_id is not None and creatorid is None:
            pass  # this is fine as-is
        elif self.creator_id is None and creatorid is None:
            pass  # this is fine as-is
        elif self.creator_id == creatorid:
            pass  # this is fine as-is
        else:
            raise SubscriptionException("creator_id: my creator_id: {self.creator_id} and passed in creatorid: {creatorid} do not match!")

        if self.subscription_id is None:
            self.subscription_id = SubscriptionFinder.get_subscription_id_or_free_tier_id(creatorid, subscriptionid)
        """ if creatorid is None we are creating an account owner """
        if self.creator_id is None:
            session.add(self)
            session.commit()
            self.creator_id = self.id
            sub = SubscriptionTrackingEntity(creator_id=self.id, users=1)
            session.add(sub)
            session.commit()
            self.subscription_tracking = [sub]
            session.commit()
            self.create_my_team(session)
            logging.info(f"User.create_me: created user: {self.id}")
            return True
        else:
            """ we are creating a regular user. they need to have
                the same subscription tracking as the account owner """
            ok = Checker.incrementOrReject(self.creator_id, "users")
            print(f"User.create_me: checker for users with my id: {self.id} and creator: {self.creator_id} returned {ok}\n\n")
            if ok:
                session.add(self)
                session.commit()
                sub = session.query(SubscriptionTrackingEntity).filter_by(creator_id=self.creator_id).first()
                self.subscription_tracking = [sub]
                session.commit()
                sub.users = sub.users + 1
                session.commit()
                logging.info(f"User.create_me: created user: {self.id}")
                return True
            else:
                return False

    def create_my_team(self,session) -> None:
        team = Team(name='My team', creator_id=self.id)
        team.create_me(self, session)

    def create_a_team(self, team:Team, session) -> None:
        team.creator_id = self.id
        team.create_me(self, session)

    def add_me_to_team(self, teamid:int, role:Roles, session) -> None:
        if not Roles.is_role(role):
            raise Exception(f"{role} is not a role")
        with session.get_bind().engine.connect() as c:
            stmt = text(f"insert into user_team_role(user_id, team_id, role_id)\
                      values({self.id}, {teamid}, '{role.value}')")
            c.execute(stmt)

    def add_me_to_project(self, projectid:int, role:Roles, session) -> None:
        if not Roles.is_role(role):
            raise Exception(f"{role} is not a role")
        with session.get_bind().engine.connect() as c:
            stmt = text(f"insert into user_project_role(user_id, project_id, role_id)\
                      values({self.id}, {projectid}, '{role.value}')")
            c.execute(stmt)

    def remove_me_from_team(self, teamid:int, session) -> None:
        with session.get_bind().engine.connect() as c:
            stmt = text(f"delete from user_team_role \
                          where user_id={self.id} and team_id={teamid})")
            c.execute(stmt)

    def remove_me_from_project(self, projectid:int, session) -> None:
        with session.get_bind().engine.connect() as c:
            stmt = text(f"delete from user_project_role where \
                          user_id={self.id} and project_id={projectid})")
            c.execute(stmt)

    def delete_team(self, teamid:int) -> bool:
        pass

    def delete_project(self, projectid:int) -> bool:
        pass

    def delete_user(self, userid:int) -> bool:
        pass

    def delete_api_key(self, apikeyid:int) -> bool:
        pass


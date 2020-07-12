import logging
from typing import Optional, List, Tuple
from application.db.roles import Roles
from application.subscriptions.account_finder import AccountFinder
from sqlalchemy.sql import text
import shutil

class OwnerMember(object):

    def __init__(self, restricted):
        self._restricted = restricted
        self._type = "project" if "Project" == type(restricted).__name__ else "team"

    def can_update_or_delete(self, uid, session) -> bool:
        logging.info(f"OwnerMember.can_update_or_delete: uid: {uid}, restricted: {self._restricted}")
        if uid == self._restricted.creator_id:
            logging.info(f"OwnerMember.can_update_or_delete: True because uid==creator_id: {uid}")
            return True
        if uid in self.get_owner_ids(session):
            logging.info(f"OwnerMember.can_update_or_delete: True because uid in owner_ids: {self.get_owner_ids(session)}")
            return True
        if  self._type == "project":
            if self._can_update_or_delete_because_team(uid, session):
                logging.info(f"OwnerMember.can_update_or_delete: True because _can_update_or_delete_because_team")
                return True
        accountid = AccountFinder.get_account_owner_id(self._restricted.creator_id)
        if uid == accountid:
            logging.info(f"OwnerMember.can_update_or_delete: True because {uid} is the account owner")
            return True
        logging.info(f"OwnerMember.can_update_or_delete: uid: {uid} cannot update or delete")
        return False

    def _can_update_or_delete_because_team(self, uid, session):
        team = self._restricted.team
        if team is not None:
            if uid == team.creator_id:
                logging.info(f"OwnerMember._can_update_or_delete_because_team: True because {uid} is team creator")
                return True
            if uid in team.get_owner_ids(session):
                logging.info(f"OwnerMember._can_update_or_delete_because_team: True because {uid} is in owner ids: {team.get_owner_ids(session)}")
                return True
        return False

    def get_owner_ids(self, session):
        return self._get_ids(Roles.OWNER.value, session)

    def get_member_ids(self, session):
        return self._get_ids(Roles.MEMBER.value, session)

    def get_viewer_ids(self, session):
        return self._get_ids(Roles.VIEWER.value, session)

    def _get_ids(self, roleid, session):
        ids = []
        with session.get_bind().engine.connect() as c:
            stmt = text(f"select user_id from user_{self._type}_role \
                          where {self._type}_id={self._restricted.id} and role_id='{roleid}'")
            logging.info(f"OwnerMember._get_ids: stmt: {stmt}")
            result = c.execute(stmt)
            for row in result:
                ids.append(row["user_id"])
        return ids

    def get_id_roles(self, session) -> List[Tuple[int,str]]:
        ids = []
        with session.get_bind().engine.connect() as c:
            stmt = text(f"select user_id, role_id from user_{self._type}_role \
                          where {self._type}_id={self._restricted.id}")
            logging.info(f"OwnerMember._get_id_roles: stmt: {stmt}")
            result = c.execute(stmt)
            for row in result:
                ids.append( (row["user_id"], row["role_id"]) )
        return ids

    def _make(self, uid, role:str, session) -> None:
        self.remove_user_with_role(uid, session)
        with session.get_bind().engine.connect() as c:
            stmt = text(f"insert into user_{self._type}_role(user_id, {self._type}_id, role_id)\
                      values({uid}, {self._restricted.id}, '{role}')")
            logging.info(f"OwnerMember._make: stmt: {stmt}")
            c.execute(stmt)

    def make_owner(self, uid, session) -> None:
        self._make(uid, Roles.OWNER.value, session)

    def make_member(self, uid, session) -> None:
        self._make(uid, Roles.MEMBER.value, session)

    def make_viewer(self, uid, session) -> None:
        self._make(uid, Roles.VIEWER.value, session)

    def remove_user_with_role(self, uid, session) -> None:
        with session.get_bind().engine.connect() as c:
            stmt = text(f"delete from user_{self._type}_role where user_id={uid} and {self._type}_id={self._restricted.id}")
            logging.info(f"OwnerMember.remove_user_with_role: stmt: {stmt}")
            c.execute(stmt)


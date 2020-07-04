import logging
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, ForeignKeyConstraint
from sqlalchemy.types import Boolean, Text
from sqlalchemy.orm import relationship
from enum import Enum

class Roles(Enum):
    OWNER = "Owner"
    MEMBER = "Member"
    VIEWER = "Viewer"

    @classmethod
    def is_role(cls, arole):
        if not arole is Roles.OWNER and not arole is Roles.MEMBER and not arole is Roles.VIEWER:
            return False
        else:
            return True


Base = declarative_base()

user_project_role_table = Table(
    "user_project_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", String(20), ForeignKey("role.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
)

user_team_role_table = Table(
    "user_team_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("role_id", String(20), ForeignKey("role.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
)

api_key_project_table = Table(
    "api_key_project",
    Base.metadata,
    Column("api_key_id", Integer, ForeignKey("api_key.id")),
    Column("project_id", Integer, ForeignKey("project.id")),
)

user_subscription_tracking_table = Table(
    "user_subscription_tracking",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("subscription_tracking_id", Integer, ForeignKey("subscription_tracking.id")),
)



class Entity(Base):
    """
        id: Entity id, numeric, unique for a given entity type, and autogenerated.
            Note that IDs are populated once session.flush() is performed.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    active = Column(Boolean, unique=False, default=True)
    public = Column(Boolean, unique=False, default=False)
    description = Column(Text)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, other):
        return other is not None and self.__class__ == other.__class__ and self.id == other.id

    def __hash__(self):
        return hash(f"{self.__class__.__name__}{self.id}")


class UserEntity(Entity):
    __tablename__ = "user"
    __mapper_args__ = {"concrete": True}

    creator_id = Column(Integer, ForeignKey("user.id"), nullable=True )
    user_name = Column(String(255))
    given_name = Column(String(100))
    family_name = Column(String(100))
    system_admin = Column(Boolean, default=False)
    subscription_id = Column(Integer, ForeignKey("subscription.id"))

    teams = relationship("TeamEntity", secondary=user_team_role_table, lazy="joined")
    projects = relationship("ProjectEntity", secondary=user_project_role_table, lazy="joined")
    subscription = relationship("SubscriptionEntity")
    subscription_tracking = relationship("SubscriptionTrackingEntity", \
            secondary=user_subscription_tracking_table, lazy="joined")


class TeamEntity(Entity):
    __tablename__ = "team"
    __mapper_args__ = {"concrete": True}

    name = Column(String(100))
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=True )

    users = relationship("UserEntity", secondary=user_team_role_table, lazy="joined")
    projects = relationship("ProjectEntity", lazy="joined")

class RoleEntity(Entity):
    __tablename__ = "role"
    __mapper_args__ = {"concrete": True}

    id = Column(String(20), primary_key=True)
    name = Column(String(20))

class ProjectEntity(Entity):
    __tablename__ = "project"
    __mapper_args__ = {"concrete": True}

    name = Column(String(100))
    creator_id = Column(Integer, ForeignKey("user.id") )
    team_id = Column(Integer, ForeignKey("team.id"))

    team = relationship("TeamEntity")
    users = relationship("UserEntity", secondary=user_project_role_table, lazy="joined")
    keys = relationship("ApiKeyEntity", secondary=api_key_project_table, lazy="joined")

class ApiKeyEntity(Entity):
    __tablename__ = "api_key"
    __mapper_args__ = {"concrete": True}

    key = Column(String(36), nullable=False )
    name = Column(String(100))
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=True )

    projects = relationship("ProjectEntity", secondary=api_key_project_table, lazy="joined")


class SubscriptionEntity(Entity):
    __tablename__ = "subscription"
    __mapper_args__ = {"concrete": True}

    users = Column(Integer, default=0 )
    """ max root count across all projects """
    roots = Column(Integer, default=0 )
    """ max projects across all teams """
    projects = Column(Integer, default=0 )
    """ max teams made by the subscription holder """
    teams = Column(Integer, default=0 )
    """ max team members in a team """
    team_members = Column(Integer, default=0 )
    """ max docs total across all roots """
    docs = Column(Integer, default=0 )
    """ max size of uploaded docs """
    each_doc_bytes = Column(Integer, default=0 )
    """
    the total number of bytes for all docs in projects
    where the creator_id is a user with this
    subscription_tracking table entry. if I upload a doc
    we look for my subscription_tracking entry and
    increment this counter. this implies that all users
    created by a subscription holder have a pointer to
    their subscription_tracking entry
    """
    total_doc_bytes = Column(Integer, default=0 )
    """ max api keys across all projects """
    api_keys = Column(Integer, default=0 )
    """ max api calls within a timeframe """
    api_calls = Column(Integer, default=0 )
    """ indicates when api_calls resets """
    api_cycle = Column(String(20), nullable=False, default="Monthly" )
    """ indicates length of a subscription -- Monthly, Annual """
    subscription_cycle = Column(String(20), nullable=False, default="Monthly" )
    name = Column(String(100))

class SubscriptionTrackingEntity(Entity):
    __tablename__ = "subscription_tracking"
    __mapper_args__ = {"concrete": True}

    users = Column(Integer, default=0 )
    roots = Column(Integer, default=0 )
    projects = Column(Integer, default=0 )
    teams = Column(Integer, default=0 )
    docs = Column(Integer, default=0 )
    total_doc_bytes = Column(Integer, default=0 )
    api_keys = Column(Integer, default=0 )
    api_calls = Column(Integer, default=0 )
    """ api_calls_current_period: identifies the current period. e.g. 'June' or '2020' """
    api_calls_current_period = Column(String(20), default=0 )
    """ this is the subscriber. all the users they create have a pointer
       to this table row, but only the user in this column owns the subscription """
    creator_id = Column(Integer, ForeignKey("user.id") )




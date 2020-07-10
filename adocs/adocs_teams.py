from application.teams.team import Team
from application.db.entities import Roles, ApiKeyEntity, SubscriptionEntity, SubscriptionTrackingEntity
from application.db.loader import Loader
from application.db.database import Database
from typing import Dict, List

class AdocsTeams(object):

    @classmethod
    def get_team(cls, id:int):
        return cls._get_thing(Team,id)

    @classmethod
    def get_team_users(cls, id:int) -> List[Dict]:
        return cls.get_context_users(Team, id)

    @classmethod
    def get_team_projects(cls, id:int) -> List[Dict]:
        loaded = Loader.load(Team, id)
        result = []
        for project in loaded.thing.projects:
            result.append( { "id":project.id, "name":project.name} )
        loaded.done()
        return result

    @classmethod
    def create_team(cls, creatorid:int, name:str, description:str) -> List[Dict]:
        loaded = Loader.load(User, creatorid)
        team = Team(name=name, description=description)
        team.create_me(loaded.thing, loaded.session)
        loaded.done()
        return team





from application.teams.team import Team
from application.users.user import User
from application.db.entities import Roles, ApiKeyEntity, SubscriptionEntity, SubscriptionTrackingEntity
from application.db.loader import Loader
from application.db.database import Database
from typing import Dict, List, Any

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
    def create_team(cls, id, teamdata:Dict[str,Any]) -> List[Dict]:
        print(f"adocs_teams.create_team: {id}, {teamdata}")
        loaded = Loader.load(User, id)
        team = Team(name=teamdata.get('name'), description=teamdata.get('description'))
        created = loaded.thing.create_a_team(team, loaded.session)
        loaded.done()
        if created:
            return team.get_dict()
        else:
            return {"error":"/app/forms/errors/cannot_create_team"}





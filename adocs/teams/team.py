import json
from flask_restful import Resource
from typing import List, Dict
from adocs.base_resource import BaseResource
from adocs.adocs import Adocs

class TeamResource(BaseResource):
    endpoint = "/team/<int:id>"

    def get(self, id) -> Dict:
        return Adocs.get_team(id)

class TeamsResource(BaseResource):
    endpoint = "/team"

    def post(self, id) -> Dict:
        parser.add_argument('name', required=True, help='/app/forms/errors/no_team_name')
        parser.add_argument('description')
        parser.add_argument('creator_id', required=True, type=int)
        teamdata = parser.parse_args()
        return Adocs.create_team(teamdata['creator_id'], teamdata['name'], teamdata['description'])

class TeamUsersResource(BaseResource):
    endpoint = "/team/<int:id>/user"

    def get(self, id) -> Dict:
        return Adocs.get_team_users(id)


class TeamProjectsResource(BaseResource):
    endpoint = "/team/<int:id>/project"

    def get(self, id) -> Dict:
        return Adocs.get_team_projects(id)



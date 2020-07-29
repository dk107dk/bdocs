import json
from flask_restful import Resource
from flask import request
from typing import List, Dict
from adocs.base_resource import BaseResource
from adocs.adocs import Adocs

class UserResource(BaseResource):
    endpoint = "/user/<int:id>"

    def get(self, id) -> Dict:
        return Adocs.get_user(id)

class UsersResource(BaseResource):
    """ gets the users created by the user identified by id """
    endpoint = "/user/<int:id>/user"

    def get(self, id) -> Dict:
        return Adocs.get_users_created_by(id)

    def post(self, id) -> Dict:
        userdata = request.get_json()
        print(f"UsersResource.post: userdata: {userdata}")
        user = Adocs.create_user(id, userdata)
        print(f"UsersResource.post: created user: {user}")
        if user is None:
            print(f"UsersResource.post: no new user created for requesting user: {id}")
            pass
        else:
            return user

class UserTeamsResource(BaseResource):
    endpoint = "/user/<int:id>/team"

    def get(self, id) -> Dict:
        return Adocs.get_user_teams(id)

    def post(self, id) -> Dict:
        teamdata = request.get_json()
        print(f"UserTeamsResource.post: teamdata: {teamdata}")
        team = Adocs.create_team(id, teamdata)
        print(f"UserTeamsResource.post: created team: {team}")
        if team is None:
            print(f"UserTeamsResource.post: no new team created for requesting user: {id}")
            pass
        else:
            return team

class UserProjectsResource(BaseResource):
    endpoint = "/user/<int:id>/project"

    def get(self, id) -> Dict:
        return Adocs.get_user_projects(id)

class UserRootsResource(BaseResource):
    endpoint = "/user/<int:id>/root"

    def get(self, id) -> Dict:
        return Adocs.get_user_roots(id)

class AddUserToTeamResource(BaseResource):
    endpoint = "/user/<int:uid>/team/<int:tid>"

    def post(self, id, tid):
        parser.add_argument('actorid', required=True, help='/app/forms/errors/no_actor_id')
        userdata = parser.parse_args()
        return Adocs.add_user_to_(userdata["actorid"], "team", tid, uid)

class AddUserToProjectResource(BaseResource):
    endpoint = "/user/<int:uid>/project/<int:tid>"

    def post(self, id, tid):
        parser.add_argument('actorid', required=True, help='/app/forms/errors/no_actor_id')
        userdata = parser.parse_args()
        return Adocs.add_user_to_(userdata["actorid"], "project", tid, uid)

class UserSubscriptionResource(BaseResource):
    endpoint = "/user/<int:id>/subscription"

    def get(self, id) -> Dict:
        return Adocs.get_user_subscription(id)

class UserSubscriptionTrackingResource(BaseResource):
    endpoint = "/user/<int:id>/subscription/tracking"

    def get(self, id) -> Dict:
        return Adocs.get_user_subscription_tracking(id)



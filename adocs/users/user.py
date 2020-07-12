import json
from flask_restful import Resource
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

    def post(self) -> Dict:
        parser.add_argument('given_name', required=True, help='/app/forms/errors/no_given_name')
        parser.add_argument('family_name', required=True, help='/app/forms/errors/no_family_name')
        parser.add_argument('user_name', required=True, help='/app/forms/errors/no_user_name')
        parser.add_argument('creator_id', type=int)
        userdata = parser.parse_args()
        user = Adocs.create_user(userdata)
        if user is None:
            pass
        else:
            return user.get_dict()

class UserTeamsResource(BaseResource):
    endpoint = "/user/<int:id>/team"

    def get(self, id) -> Dict:
        return Adocs.get_user_teams(id)

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



import json
from flask_restful import Resource
from typing import List, Dict
from adocs.base_resource import BaseResource
from adocs.adocs import Adocs

class ProjectResource(BaseResource):
    endpoint = "/project/<int:id>"

    def get(self, id) -> Dict:
        return Adocs.get_project(id)

class ProjectsResource(BaseResource):
    endpoint = "/project"

    def post(self, id) -> Dict:
        parser.add_argument('name', required=True, help='/app/forms/errors/no_project_name')
        parser.add_argument('description')
        parser.add_argument('creator_id', required=True, type=int)
        projectdata = parser.parse_args()
        return Adocs.create_project(projectdata['creator_id'], projectdata['name'], projectdata['description'])

class ProjectUsersResource(BaseResource):
    endpoint = "/project/<int:id>/user"

    def get(self, id) -> List[Dict]:
        return Adocs.get_project_users(id)

class ProjectRootsResource(BaseResource):
    endpoint = "/project/<int:id>/root"

    def get(self, id) -> List:
        return Adocs.get_project_roots(id)

class RootInfoResource(BaseResource):
    endpoint = "/project/<int:id>/root/<name>"

    def get(self, id:int, name:str) -> Dict:
        return Adocs.get_project_rootinfo(id, name)

class ProjectKeysResource(BaseResource):
    endpoint = "/project/<int:id>/key"

    def get(self, id:int) -> List[Dict]:
        return Adocs.get_project_keys(id)

    def post(self, id) -> Dict:
        parser.add_argument('name', required=True, help='/app/forms/errors/no_key_name')
        parser.add_argument('description')
        parser.add_argument('creator_id', required=True, type=int)
        keydata = parser.parse_args()
        return Adocs.create_api_key(keydata['creator_id'], keydata['name'], keydata['description'])

class TreeResource(BaseResource):
    endpoint = "/project/<int:id>/root/<name>/tree"

    def get(self, id:int, name:str) -> Dict:
        return Adocs.get_tree(id, name)


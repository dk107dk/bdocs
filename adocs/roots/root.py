import json
from flask_restful import Resource
from typing import List, Dict
from adocs.base_resource import BaseResource
from adocs.adocs import Adocs

class ProjectResource(BaseResource):
    endpoint = "/project/<int:id>"

    def get(self, id) -> Dict:
        return Adocs.get_project(id)

class ProjectUsersResource(BaseResource):
    endpoint = "/project/<int:id>/user"

    def get(self, id) -> List[Dict]:
        return Adocs.get_project_users(id)

class ProjectRootsResource(BaseResource):
    endpoint = "/project/<int:id>/root"

    def get(self, id) -> List:
        return Adocs.get_project_roots(id)


class ProjectKeysResource(BaseResource):
    endpoint = "/project/<int:id>/key"

    def get(self, id:int) -> List[Dict]:
        return Adocs.get_project_keys(id)



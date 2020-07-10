from application.projects.project import Project
from application.db.entities import ApiKeyEntity
from application.db.loader import Loader
from application.roots.doc_root_management import DocRootManagement
from bdocs.building_metadata import BuildingMetadata
from typing import Dict, List


class AdocsProjects(object):

    @classmethod
    def get_project(cls, id:int):
        return cls._get_thing(Project,id)

    @classmethod
    def create_project(cls, creatorid:int, name:str, description:str) -> List[Dict]:
        loaded = Loader.load(User, creatorid)
        project = Project(name=name, description=description)
        project.create_me(loaded.thing, loaded.session)
        loaded.done()
        return project

    @classmethod
    def get_project_keys(cls, id:int):
        loaded = Loader.load(Project, id)
        result = []
        for key in loaded.thing.keys:
            result.append( { "id":key.id, "key":key.key, "name":key.name })
        loaded.done()
        return result

    @classmethod
    def get_api_key(cls, id:int):
        return cls._get_thing(ApiKeyEntity,id)

    @classmethod
    def create_api_key(cls, creatorid:int, name:str, description:str) -> List[Dict]:
        loaded = Loader.load(User, creatorid)
        key = ApiKey(name=name, description=description)
        key.create_me(loaded.thing, loaded.session)
        loaded.done()
        return key

    @classmethod
    def get_project_users(cls, id:int) -> List[Dict]:
        return cls.get_context_users(Project, id)

    @classmethod
    def get_project_roots(cls, id:int) -> List[Dict]:
        mgmt = DocRootManagement()
        loaded = Loader.load(Project, id)
        pid = id
        tid = loaded.thing.team.id
        uid = loaded.thing.team.creator_id
        loaded.done()
        roots = mgmt.get_roots(uid, tid, pid)
        roots = [ _[0] for _ in roots]
        return roots

    @classmethod
    def get_project_rootinfo(cls, id:int, name:str) -> Dict:
        mgmt = DocRootManagement()
        uid,tid,pid = cls._get_uid_tid_pid(id)
        config = mgmt.get_config_of(uid, tid, pid)
        metadata = BuildingMetadata(config)
        rootinfo = metadata.get_root_info(name)
        s = rootinfo.to_json()
        print(f"app.roots: root names: {rootinfo} ")
        return s



from adocs.adocs_users import AdocsUsers
from adocs.adocs_teams import AdocsTeams
from adocs.adocs_projects import AdocsProjects
from adocs.adocs_roles import AdocsRoles
from adocs.adocs_subscriptions import AdocsSubscriptions
from adocs.adocs_docpath import AdocsDocpath
from application.projects.project import Project
from application.teams.team import Team
from application.users.user import User
from application.db.entities import ApiKeyEntity
from application.db.loader import Loader, Loaded
from typing import Dict, Tuple

class Adocs(AdocsUsers,
            AdocsTeams,
            AdocsProjects,
            AdocsRoles,
            AdocsSubscriptions,
            AdocsDocpath):

    @classmethod
    def _get_loaded( cls, classname, id:int) -> Loaded:
        c = None
        if classname == "team":
            c = Team
        elif classname == "project":
            c = Project
        elif classname == "user":
            c = User
        elif classname == "api_key":
            c = ApiKeyEntity
        return Loader.load(c, id)

    @classmethod
    def _get_thing(cls, aclass, id:int) -> Dict:
        loaded = Loader.load(aclass, id)
        loaded.thing.id
        asdict = loaded.thing.get_dict()
        loaded.done()
        return asdict

    @classmethod
    def _get_things_by_creator(cls, aclass, id:int) -> Dict:
        loaded = Loader.load_items_by_creator(aclass, id)
        thing = loaded.thing
        print(f"Adocs._get_things_by_creator: thing is: {thing}")
        ds = {}
        for u in thing:
            uid = u.id
            ds[uid] = u.get_dict()
        print(f"Adocs._get_things_by_creator: results are: {ds}")
        loaded.done()
        return ds

    @classmethod
    def _get_uid_tid_pid(cls, id:int) -> Tuple[int,int,int]:
        loaded = Loader.load(Project, id)
        pid = id
        tid = loaded.thing.team.id
        uid = loaded.thing.team.creator_id
        loaded.done()
        return (uid,tid,pid)


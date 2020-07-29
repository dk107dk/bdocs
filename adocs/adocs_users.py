from application.users.user import User
from application.teams.team import Team
from application.projects.project import Project
from application.db.entities import Roles
from application.db.loader import Loader
from application.db.database import Database
from application.subscriptions.account_finder import AccountFinder
from application.roots.doc_root_management import DocRootManagement
from typing import Dict, List, Type, Union, Tuple, Optional, NewType
from contextlib import closing

STR_OR_ID = NewType('STR_OR_ID', Union[str,int])

class AdocsUsers(object):

    @classmethod
    def get_user(cls, id:int):
        return cls._get_thing(User,id)

    @classmethod
    def get_users_created_by(cls, id:int):
        return cls._get_things_by_creator(User, id)

    @classmethod
    def get_user_subscription(cls, id:int):
        loaded = Loader.load(User, id)
        result = loaded.thing.subscription.get_dict()
        loaded.done()
        return result

    @classmethod
    def create_user(cls, id, userdata:Dict[str,STR_OR_ID]) -> Dict:
        subscription_id = None
        if id is not None:
            sub = cls.get_user_subscription(id)
            print(f"Adocs.create_user: sub: {sub}")
            subscription_id = sub.get('id')
        user = User(
                given_name=userdata.get('given_name'),
                family_name=userdata.get('family_name'),
                user_name=userdata.get('user_name'),
                creator_id=id,
                subscription_id=subscription_id
        )
        engine = Database().engine
        udict = None
        with closing(engine.session()) as session:
            user.create_me(session)
            session.commit()
            print(f'Adocs.create_user: created name: {user.given_name}')
            udict = user.get_dict()
            print(f'Adocs.create_user: created dict: {udict}')
        engine.dispose()
        return udict

    @classmethod
    def get_user_subscription_tracking(cls, id:int):
        loaded = Loader.load(User, id)
        result = loaded.thing.subscription_tracking[0].get_dict()
        loaded.done()
        return result

    @classmethod
    def remove_user_from(cls, project_or_team:str, tid:int, uid:int) -> None:
        loaded = Loader.load(User, uid)
        user = loaded.thing
        session = loaded.session
        if project_or_team == "team":
            user.remove_me_from_team(tid, session)
        else:
            user.remove_me_from_project(tid, session)
        loaded.done()

    @classmethod
    def add_user_to(cls, actorid:int, project_or_team:str, tid:int, uid:int) -> bool:
        loaded = cls._get_loaded(project_or_team, anid)
        b = loaded.thing.can_update_or_delete(actorid,loaded.session)
        if not b:
            return False
        loaded = Loader.load(User, uid)
        user = loaded.thing
        session = loaded.session
        if project_or_team == "team":
            user.add_me_to_team(tid, Roles.MEMBER, session)
        else:
            user.add_me_to_project(tid, Roles.MEMBER, session)
        loaded.done()
        return True

    @classmethod
    def get_user_teams(cls, id:int) -> List[Dict]:
        loaded = Loader.load(User, id)
        result = []
        for team in loaded.thing.teams:
            result.append( { "id":team.id, "name":team.name } )
        loaded.done()
        return result

    @classmethod
    def get_user_projects(cls, id:int) -> List[Dict]:
        print(f"Adocs_users.get_user_projects: {id}")
        loaded = Loader.load(User, id)
        result = []
        for project in loaded.thing.projects:
            result.append( { "id":project.id, "name":project.name, "team_id":project.team_id, "team_name": project.team.name } )
        loaded.done()
        return result

    @classmethod
    def get_user_roots(cls, id:int) -> List[Dict]:
        print(f"Adocs_users.get_user_roots: {id}")
        uid = AccountFinder.get_account_owner_id( str(id) )
        mgmt = DocRootManagement()
        loaded = Loader.load(User, id)
        result = []
        for project in loaded.thing.projects:
            pid = project.id
            project_name = project.name
            tid = project.team.id
            team_name = project.team.name
            roots = mgmt.get_roots(uid, tid, pid)
            for _ in roots:
                result.append({
                                "project_id":pid, "project_name":project.name,
                                "team_id":tid, "team_name": team_name,
                                "root_name":_[0]
                             })
        loaded.done()
        return result


    @classmethod
    def get_context_users(cls, thingtype:Type[Union[Project,Team]], id:int) -> List[Dict]:
        loaded = Loader.load(thingtype, id)
        result = []
        for user in loaded.thing.users:
            result.append( { "id":user.id, "given_name":user.given_name,
                             "family_name":user.family_name, "user_name": user.user_name } )
        loaded.done()
        return result




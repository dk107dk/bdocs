from flask_restful import Resource
from adocs.users.user import (UserResource,
                              UsersResource,
                              UserTeamsResource,
                              UserSubscriptionResource,
                              UserSubscriptionTrackingResource,
                              AddUserToTeamResource,
                              UserProjectsResource,
                              UserRootsResource,
                              AddUserToProjectResource)
from adocs.teams.team import TeamResource, TeamUsersResource, TeamProjectsResource
from adocs.docpaths.docpath import (DocpathResource,
                                   DocpathJsonResource,
                                   DocpathTokensResource,
                                   DocpathLabelsResource,
                                   DocpathInternalLabelsResource,
                                   DocpathListResource,
                                   DocpathListRootResource)
from adocs.projects.project import (ProjectResource,
                                   ProjectUsersResource,
                                   ProjectRootsResource,
                                   ProjectKeysResource,
                                   RootInfoResource,
                                   TreeResource)
from adocs.utils import DateUtils
from typing import List, Dict, Callable
import logging

class Resources(object):

    def get_resources(self) -> List[Resource]:
        rs = [
                UserResource, UsersResource, UserTeamsResource,
                UserSubscriptionResource, UserSubscriptionTrackingResource,
                AddUserToProjectResource, AddUserToTeamResource,
                UserProjectsResource, UserRootsResource,
                TeamResource, TeamUsersResource, TeamProjectsResource,
                ProjectResource, ProjectUsersResource, ProjectRootsResource, ProjectKeysResource,
                TreeResource, RootInfoResource,
                DocpathResource, DocpathJsonResource, DocpathListResource, DocpathListRootResource,
                DocpathLabelsResource, DocpathInternalLabelsResource, DocpathTokensResource
        ]
        du = DateUtils()
        for r in rs:
            #logging.info
            print(f"Resources.get_resources: applying datetimes fix wrapper to {r} at {r.endpoint}")
            ms = [method_name for method_name in dir(r) if callable(getattr(r, method_name))]
            for m in ['get','post','patch','put','delete','head']:
                try:
                    setattr( r, m, du._wrap_fix_datetimes(getattr(r, m)) )
                except:
                    pass
        return rs


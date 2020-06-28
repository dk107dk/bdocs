import datetime
import os
import json
from flask_restful import Resource
from typing import List, Dict

class ReachableResource(Resource):

    def __init__(self):
        self._endpoint = None

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @endpoint.setter
    def endpoint(self, v) -> None:
        self._endpoint = v


class UserResource(ReachableResource):
    """
    //
    // /user {noun}
    // /login {do the needful with auth0}
    // /session {get token, refresh token, etc.}
    //
    """
    def get(self, id) -> List[Dict]:
        return []

class TeamResource(ReachableResource):
    """
    //
    // /team {noun; users working on projects}
    // /team/user {team users are owners and/or members within team and its projects}
    //
    """
    def get(self, id) -> List[Dict]:
        return []

class ProjectResource(ReachableResource):
    """
    //
    // /team/project {noun; a set of roots defined by a config.ini}
    // /team/project/config {everything in config.ini not tied to a root}
    // /team/project/role  {owner, member, reader}
    // /team/project/role/user {one of the team members or a reader}
    // /team/project/root {noun; manage roots defined in config.ini}
    // /team/project/apikey {create and manage one or more api keys for the project}
    //
    """
    def get(self, id) -> List[Dict]:
        return []

class RootResource(ReachableResource):
    """
    //
    // /team/project/root/tag {create a git tag, if enabled}
    // /team/project/root/accepts
    // /team/project/root/formats
    // /team/project/root/converters  {from/to on the fly convertions, if enabled}
    // /team/project/root/feature
    // /team/project/root/export {download as zip, push to remote git, if enabled}
    // /team/project/root/upload {upload as zip, upload file}
    // /team/project/root/tree {get json tree representations of root}
    // /team/project/root/search {find doc metadata in root, if enabled}
    //
    """
    def get(self, id) -> List[Dict]:
        return []

class DocpathResource(ReachableResource):
    """
    //
    // /team/project/doc {noun; in raw, transformed or converted form}
    // /team/project/doc/diff {comparison of two docs}
    // /team/project/doc/version {versions of a doc, if enabled}
    // /team/project/metadata {data about a doc at a docpath}
    // /team/project/labels {noun}
    // /team/project/tokens {noun; tokens in editable, untransformed json}
    //
    """
    def get(self, id) -> List[Dict]:
        return []


class Resources(object):

    def getResources(self) -> List[ReachableResource]:
        return [UserResource(), TeamResource(), ProjectResource(), RootResource() ]






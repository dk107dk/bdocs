from flask_restful import Resource
from typing import List, Dict
from adocs.base_resource import BaseResource
from adocs.adocs import Adocs
from flask import request

class DocpathResource(BaseResource):
    endpoint = "/project/<int:id>/doc/<path:docpath>"

    def get(self, id:int, docpath:str) -> Dict:
        docpath = "/" + docpath
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: {docpath}" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_doc_at_path(id, docpath, roots)

class DocpathListResource(BaseResource):
    endpoint = "/project/<int:id>/list/<path:docpath>"

    def get(self, id:int, docpath:str) -> List:
        docpath = "/" + docpath
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: {docpath}" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_docs_at_path(id, docpath, roots)

class DocpathListRootResource(BaseResource):
    endpoint = "/project/<int:id>/listroot"

    def get(self, id:int) -> List:
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: /" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_docs_at_path(id, "/", roots)

class DocpathJsonResource(BaseResource):

    endpoint = "/project/<int:id>/json/<path:docpath>"

    def get(id:int, docpath:str):
        docpath = "/" + docpath
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: {docpath}" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_docs_as_json_at_path(id, docpath, roots)

class DocpathLabelsResource(BaseResource):

    endpoint = "/project/<int:id>/labels/<path:docpath>"

    def get(id:int, docpath:str):
        docpath = "/" + docpath
        recurse = request.args.get('recurse')
        if recurse is None:
            recurse = True
        else:
            recurse = False if recurse == "false" else True
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: {docpath}" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_labels_at_path(id, docpath, roots, recurse)


class DocpathInternalLabelsResource(BaseResource):

    endpoint = "/internal/labels/<path:docpath>"

    def get(cls, docpath:str):
        docpath = "/" + docpath
        recurse = request.args.get('recurse')
        if recurse is None:
            recurse = True
        else:
            recurse = False if recurse == "false" else True
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: {docpath}" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_internal_labels_at_path(docpath, roots, recurse)


class DocpathTokensResource(BaseResource):

    endpoint = "/project/<int:id>/tokens/<path:docpath>"

    def get(id:int, docpath:str):
        docpath = "/" + docpath
        recurse = request.args.get('recurse')
        if recurse is None:
            recurse = True
        else:
            recurse = False if recurse == "false" else True
        roots = request.args.get('roots')
        if roots is None:
            pass
        else:
            roots = roots.split(",")
        print(f"> request path: {request.path}; docpath: {docpath}" )
        print(f"> limit to roots: {roots}")
        return Adocs.get_tokens_at_path(id, docpath, roots, recurse)


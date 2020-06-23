import datetime
import os
import json
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_cors import CORS, cross_origin
from cdocs.cdocs import Cdocs
from cdocs.cdocs import Cdocs
from cdocs.context import Context
from cdocs.context_metadata import ContextMetadata
from bdocs.bdocs import Bdocs
from bdocs.bdocs_config import BdocsConfig
from bdocs.building_metadata import BuildingMetadata
from bdocs.block import Block

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/tree/<path:root>')
def tree(root:str):
    print(f"root: {root}" )
    print(f"current working directory is {os.getcwd()}")
    config = BdocsConfig()
    metadata = BuildingMetadata(config)
    building = Block(metadata)
    tree = building.get_doc_tree(root)
    print(f"tree at {tree} found ")
    if tree is None:
        tree = "get_doc_tree returned None"
    return tree

@app.route('/roots')
def roots():
    config = BdocsConfig()
    metadata = BuildingMetadata(config)
    roots = metadata.root_names
    print(f"app.roots: root names: {roots} ")
    return { "roots":roots }

@app.route('/rootinfo/<path:root>')
def rootinfo(root:str):
    config = BdocsConfig()
    metadata = BuildingMetadata(config)
    rootinfo = metadata.get_root_info(root)
    s = rootinfo.to_json()
    print(f"app.roots: root names: {rootinfo} ")
    return s

@app.route('/docs/<path:docpath>')
def docs(docpath:str):
    docpath = "/" + docpath
    roots = request.args.get('roots')
    if roots is None:
        pass
    else:
        roots = roots.split(",")
    print(f"> request path: {request.path}; docpath: {docpath}" )
    print(f"> current working directory is {os.getcwd()}")
    print(f"> limit to roots: {roots}")
    metadata = ContextMetadata()
    context = Context(metadata)
    doc = ""
    if roots is None:
        doc = context.get_doc(docpath)
    else:
        doc = context.get_doc_from_roots(roots,docpath)
    print(f"cdocs at {docpath} found ")
    if doc is None:
        doc = "doc not found and no 'not found' doc returned"
    return doc

@app.route('/json/<path:docpath>')
def json(docpath:str):
    docpath = "/" + docpath
    roots = request.args.get('roots')
    if roots is None:
        pass
    else:
        roots = roots.split(",")
    print(f"request path: {request.path}; docpath: {docpath}" )
    print(f"current working directory is {os.getcwd()}")
    print(f"limit to roots: {roots}")
    metadata = ContextMetadata()
    context = Context(metadata)
    doc = ""
    if roots is None:
        doc = context.get_doc(docpath)
    else:
        doc = context.get_doc_from_roots(roots,docpath)
    print(f"cdocs at {docpath} found ")
    if doc is None:
        doc = "doc not found and no 'not found' doc returned"
    try:
        json.load(doc)
    except:
        doc = { "doc": doc }
    return doc

@app.route('/labels/<path:docpath>')
def labels(docpath:str):
    docpath = "/" + docpath
    recurse = request.args.get('recurse')
    if recurse is None:
        recurse = True
    else:
        recurse = False if recurse == "false" else True
    print(f"request path: {request.path}; docpath: {docpath}" )
    print(f"current working directory is {os.getcwd()}")
    metadata = ContextMetadata()
    context = Context(metadata)
    doc = context.get_labels(docpath, recurse)
    print(f"cdocs at {docpath} found ")
    if doc is None:
        doc = "doc not found and no 'not found' doc returned"
    return doc

@app.route('/tokens/<path:docpath>')
def tokens(docpath:str):
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
    print(f"request path: {request.path}; docpath: {docpath}" )
    print(f"current working directory is {os.getcwd()}")
    metadata = ContextMetadata()
    context = Context(metadata)
    if roots is None:
        doc = context.get_tokens(docpath, recurse)
    else:
        doc = context.get_tokens_from_roots(roots,docpath, recurse)
    print(f"cdocs at {docpath} found ")
    if doc is None:
        doc = "doc not found and no 'not found' doc returned"
    return doc


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', help='app help')
    args = parser.parse_args()
    args = vars(args)
    try:
        os.environ['DATABASE'] = args["database"]
    except:
        pass
    database = os.environ.get('DATABASE')
    print(f'env db: {database}')
    app.run(debug=True)

import datetime
import os
import json
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_cors import CORS, cross_origin
from adocs.resources import Resources
from adocs.users.user import UserResource


app = Flask(__name__)
CORS(app)
api = Api(app)


for r in Resources().get_resources():
    print(f"adding resource: {r.endpoint} = {r}")
    api.add_resource(r, r.endpoint )




#print(f"iterating rules from {app.url_map}")
#for rule in app.url_map.iter_rules():
#    print(f"........... RULE: {rule}")



if __name__ == '__main__':
    app.run(debug=True)



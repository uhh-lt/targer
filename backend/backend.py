#!/usr/bin/env python3

"""be.py: Description."""
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api, Resource, reqparse
from flask import make_response
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import json
from flask import jsonify
import json

"""Models"""

from Model import Model
from ModelNewES import ModelNewES
from ModelNewWD import ModelNewWD
import configparser
from elasticsearch import Elasticsearch
from es_utils import search_in_es
modelNewES = ModelNewES()

modelNewWD = ModelNewWD()

modelIBM = Model("IBM.h5")
#We must call this cause of a keras bug
#https://github.com/keras-team/keras/issues/2397
modelIBM.label("Therefore fixed punishment will")

modelCombo = Model("COMBO.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelCombo.label("Therefore fixed punishment will")

modelES = Model("ES.h5")
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelES.label("Therefore fixed punishment will")

modelWD = Model("WD.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelWD.label("Therefore fixed punishment will")

modelES_dep = Model("ES_dep.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelES_dep.label("Therefore fixed punishment will")

modelWD_dep = Model("WD_dep.h5")
# # We must call this cause of a keras bug
# # https://github.com/keras-team/keras/issues/2397
modelWD_dep.label("Therefore fixed punishment will")

config_parser = configparser.ConfigParser()
config_parser.read('config.ini')
config = config_parser['DEV']

ES_SERVER = {"host": config["es_host"], "port": int(config["es_port"])}
INDEX_NAME = 'arguments'
es = Elasticsearch(hosts=[ES_SERVER])

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

reversed = True

if(reversed):
	app.wsgi_app = ReverseProxied(app.wsgi_app)
	template2 = dict(swaggerUiPrefix=LazyString(lambda : request.environ.get('HTTP_X_SCRIPT_NAME', '')))
	swagger = Swagger(app, template=template2)
else:
	swagger = Swagger(app)

api = Api(app)

class ClassifyNewWD(Resource):
    def post(self):
       """
       Classifies input text to argument structure (Essays model, fasttext - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelNewWD.label(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class ClassifyNewPE(Resource):
    def post(self):
       """
       Classifies input text to argument structure (Essays model, fasttext embeddings)

       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelNewES.label(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class ClassifyES(Resource):
    def post(self):
       """
       Classifies input text to argument structure (Essays model, fasttext embeddings)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify 
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelES.label_with_probs(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response
       
class ClassifyWD(Resource):
    def post(self):
       """
       Classifies input text to argument structure (WebD model, fasttext - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelWD.label_with_probs(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class ClassifyES_dep(Resource):
    def post(self):
       """
       Classifies input text to argument structure (Essays model, dependency based)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelES_dep.label_with_probs(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class ClassifyWD_dep(Resource):
    def post(self):
       """
       Classifies input text to argument structure (WebD model, dependency based)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelWD_dep.label_with_probs(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class ClassifyIBM(Resource):
    def post(self):
       """
       Classifies input text to argument structure (IBM model, fasttext - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelIBM.label_with_probs(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class ClassifyCombo(Resource):
    def post(self):
       """
       Classifies input text to argument structure (Combo model - big dataset)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify
           example: Quebecan independence is justified. In the special episode in Japan, his system is restored by a doctor who wishes to use his independence for her selfish reasons.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: argument-structure
             properties:
               argument-structure:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelCombo.label_with_probs(inputtext)
       response = make_response(jsonify(result))
       response.headers['content-type'] = 'application/json'
       return response

class SearchES(Resource):
    def post(self):
       """
       Argument Retrieval endpoint
       ---
       consumes:
         - application/json
       parameters:
         - in: body
           name: search_object
           description: Request consists of search query, minimum confidence score, entities to search
           schema:
             type: object
             required:
               - search_query
               - confidence
               - where_to_search
             properties:
               search_query:
                 type: string
                 example: coffee
               confidence:
                 type: integer
                 example: 75
               where_to_search:
                 type: array
                 items:
                   type: string
                 example:
                   - text
                   - premise
       responses:
           200:
             description: OK
        """

       request_data = request.json
       search_query = request_data['search_query']
       confidence = request_data['confidence']
       where_to_search = request_data['where_to_search']

       result = search_in_es(es, INDEX_NAME, str(search_query), where_to_search, confidence)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response

api.add_resource(ClassifyES, '/classifyES')
api.add_resource(ClassifyWD, '/classifyWD')
api.add_resource(ClassifyES_dep, '/classifyES_dep')
api.add_resource(ClassifyWD_dep, '/classifyWD_dep')
api.add_resource(ClassifyIBM, '/classifyIBM')
api.add_resource(ClassifyCombo, '/classifyCombo')
api.add_resource(ClassifyNewPE, '/classifyNewPE')
api.add_resource(ClassifyNewWD, '/classifyNewWD')
api.add_resource(SearchES, '/search_arguments')

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='0.0.0.0', port=6000,debug=True)



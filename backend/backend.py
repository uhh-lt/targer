#!/usr/bin/env python3

"""be.py: Description."""
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api, Resource, reqparse
from flask import make_response
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import json

from Model import Model
from ModelES import ModelES
from ModelWD import ModelWD
from ModelESk import ModelESk
from ModelWDk import ModelWDk

model = Model()
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
model.label("Therefore fixed punishment will")

modelES = ModelES()
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelES.label("Therefore fixed punishment will")

modelWD = ModelWD()
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelWD.label("Therefore fixed punishment will")

modelESk = ModelESk()
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelESk.label("Therefore fixed punishment will")

modelWDk = ModelWDk()
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
modelWDk.label("Therefore fixed punishment will")

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



@app.route("/")
def hello():
    return "Hello World!"

class Inputtext(Resource):
    def post(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (default model)
       ---
       parameters:
         - in: path
           name: inputtext
           type: string
           required: true
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       result = model.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response

class InputtextES(Resource):
    def post(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (ES model)
       ---
       parameters:
         - in: path
           name: inputtext
           type: string
           required: true
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       result = modelES.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response

class InputtextWD(Resource):
    def post(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (WD model)
       ---
       parameters:
         - in: path
           name: inputtext
           type: string
           required: true
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       result = modelWD.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response

class InputtextESk(Resource):
    def post(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (EDk model)
       ---
       parameters:
         - in: path
           name: inputtext
           type: string
           required: true
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       result = modelESk.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response

class InputtextWDk(Resource):
    def post(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (WDk model)
       ---
       parameters:
         - in: path
           name: inputtext
           type: string
           required: true
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       result = modelWDk.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response


class ClassifyES(Resource):
    def post(self):
       """
       Takes a input sequence and assigns label with highes probability (ES model)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify 
           example: This is an example sentence. You can paste in any other text, because this is a text field. The quotes are not needed.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelES.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response
       
class ClassifyWD(Resource):
    def post(self):
       """
       Takes a input sequence and assigns label with highes probability (WD model)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify 
           example: This is an example sentence. You can paste in any other text, because this is a text field. The quotes are not needed.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelWD.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response
       
class ClassifyESk(Resource):
    def post(self):
       """
       Takes a input sequence and assigns label with highes probability (ESk model)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify 
           example: This is an example sentence. You can paste in any other text, because this is a text field. The quotes are not needed.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelESk.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response
       
class ClassifyWDk(Resource):
    def post(self):
       """
       Takes a input sequence and assigns label with highes probability (WDk model)
       ---
       consumes:
         - text/plain
       parameters:
         - in: body
           name: text
           type: string
           required: true
           description: Text to classify 
           example: This is an example sentence. You can paste in any other text, because this is a text field. The quotes are not needed.
       responses:
         200:
           description: A list of tagged tokens annotated with labels
           schema:
             id: Returntext
             properties:
               returntext:
                 type: string
                 description: JSON-List
                 default: No input text set
        """
       inputtext = request.get_data().decode('UTF-8')
       result = modelWDk.label(inputtext)
       response = make_response(result)
       response.headers['content-type'] = 'application/json'
       return response
       
api.add_resource(Inputtext, '/inputtext/<inputtext>')
api.add_resource(InputtextES, '/inputtextES/<inputtext>')
api.add_resource(InputtextWD, '/inputtextWD/<inputtext>')
api.add_resource(InputtextESk, '/inputtextESk/<inputtext>')
api.add_resource(InputtextWDk, '/inputtextWDk/<inputtext>')
api.add_resource(ClassifyES, '/classifyES')
api.add_resource(ClassifyWD, '/classifyWD')
api.add_resource(ClassifyESk, '/classifyESk')
api.add_resource(ClassifyWDk, '/classifyWDk')


app.run(host='0.0.0.0', port=6000,debug=False)


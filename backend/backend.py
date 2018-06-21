#!/usr/bin/env python3

"""be.py: Description."""
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api, Resource
from flask import make_response
from nltk.tokenize import sent_tokenize, word_tokenize
import random
import json

from Model import Model

model = Model()
# We must call this cause of a keras bug
# https://github.com/keras-team/keras/issues/2397
model.label("Therefore fixed punishment will")


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
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.json_encoder = LazyJSONEncoder

template2 = dict(swaggerUiPrefix=LazyString(lambda : request.environ.get('HTTP_X_SCRIPT_NAME', '')))

api = Api(app)
swagger = Swagger(app, template=template2)


@app.route("/")
def hello():
    return "Hello World!"

class Inputtext(Resource):
    def get(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (mockup)
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
    def post(self, inputtext):
       """
       Takes a input sequence and assigns label with highes probability (mockup)
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


api.add_resource(Inputtext, '/inputtext/<inputtext>')

app.run(host='0.0.0.0', port=6000,debug=False)



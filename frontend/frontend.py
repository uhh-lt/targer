#!/usr/bin/env python3

"""be.py: Description."""
from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flask_restful import Api
import json

"""Front-End"""
from flask import render_template
from json import JSONDecodeError
import requests
from elasticsearch import Elasticsearch
import re
import json

"""Spacy"""
import spacy

nlp = spacy.load('xx')
# path = "arg-mining-ltcpu/"
path = "/"


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

ES_SERVER = {"host": "0.0.0.0", "port": 9203}
INDEX_NAME = 'arguments'
es = Elasticsearch(hosts=[ES_SERVER])

reversed = True

if (reversed):
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    template2 = dict(swaggerUiPrefix=LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')))
    swagger = Swagger(app, template=template2)
else:
    swagger = Swagger(app)

api = Api(app)


class Sender:
    def send(self, text, classifier):

        if classifier == "WD":
            url = "http://backend:6000/classifyWD"
        elif classifier == "WD_dep":
            url = "http://backend:6000/classifyWD_dep"
        elif classifier == "ES":
            url = "http://backend:6000/classifyES"
        elif classifier == "ES_dep":
            url = "http://backend:6000/classifyES_dep"
        elif classifier == "IBM":
            url = "http://backend:6000/classifyIBM"
        elif classifier == "Combo":
            url = "http://backend:6000/classifyCombo"

        try:
            r = requests.post(url, data=text.encode("utf-8"))
            return r.json()
        except JSONDecodeError:
            print("!!!!", len(text), text)
            pass


sender = Sender()


@app.route('/')
def index():
    return render_template('displacy.html', title="Argument Entity Visualizer", page="index", path=path)


@app.route('/search_text', methods=['POST'])
def search_text():
    text = request.form.get('username')
    where_to_seach = request.form.getlist('where[]') # List like ['claim', 'text']
    return search_in_es(text)


@app.route('/label_text', methods=['POST'])
def background_process_arg():
    text = request.form.get('username')

    data = []

    # Arg-Mining Tags
    classifier = request.form.get('classifier')
    doc = sender.send(text, classifier)
    currentPos = 0
    for sentence in doc:
        for token in sentence:
            start = text.find(token["token"], currentPos)
            end = start + len(token["token"])
            currentPos = end
            currentWord = {}
            currentWord['start'] = start
            currentWord['end'] = end
            currentWord['type'] = token["label"]
            data.append(currentWord)

    data = do_label_arg(data)

    doc = nlp(text)
    for ent in doc.ents:
        entry = {'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
        data.append(entry)

    return json.dumps(data)


def do_label_arg(marks):
    # print("marks:" + str(marks))
    marks_new = []
    for i, item in enumerate(marks):
        # for (var i = 0; i < marks.length; i++):
        if i > 0 and i + 1 < len(marks):
            # Start Label
            if marks[i]['type'][0] == "P" and marks[i - 1]['type'][0] != marks[i]['type'][0]:
                mark = {'type': "PREMISE", 'start': marks[i]['start']}
                marks_new.append(mark)
            elif marks[i]['type'][0] == "C" and marks[i - 1]['type'][0] != marks[i]['type'][0]:
                mark = {'type': "CLAIM", 'start': marks[i]['start']}
                marks_new.append(mark)
                # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                if marks[i]['type'][0] != marks[i + 1]['type'][0]:
                    mark = marks_new.pop()
                    mark['end'] = marks[i]['end']
                    marks_new.append(mark)
        elif i == 0 and i + 1 < len(marks):
            # Start Label
            if marks[i]['type'][0] == "P":
                mark = {'type': "PREMISE", 'start': marks[i]['start']}
                marks_new.append(mark)
            elif (marks[i]['type'][0] == "C"):
                mark = {'type': "CLAIM", 'start': marks[i]['start']}
                marks_new.append(mark)
            # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                if marks[i]['type'][0] != marks[i + 1]['type'][0]:
                    mark = marks_new.pop()
                    mark['end'] = marks[i]['end']
                    marks_new.append(mark)
        elif i == 0 and i + 1 == marks.length:
            # End Label
            if marks[i]['type'][0] == "P" or marks[i]['type'][0] == "C":
                mark['end'] = marks[i]['end']
                marks_new.append(mark)
    return marks_new


def search_in_es(query):
    docs = []
    res = es.search(index=INDEX_NAME, body={"from": 0, "size": 25,
                                            "query": {
                                                "nested": {
                                                    "path": "sentences",
                                                    "score_mode": "avg",
                                                    "query": {
                                                        "bool": {
                                                            "must": [
                                                                {"match": {"sentences.text": query[:100]}}
                                                            ]
                                                        }
                                                    }
                                                }
                                            },
                                            "highlight": {
                                                "pre_tags": [""],
                                                "post_tags": [""],
                                                "fields": {
                                                    "sentences.text": {
                                                        "type": "plain",
                                                        "fragment_size": 125,
                                                        "number_of_fragments": 1,
                                                        "fragmenter": "simple"
                                                    }
                                                }
                                            }})

    query_words = query[:100].strip().split()
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:

        doc = {}
        text_full = ""


        arguments_positions = []
        entity_positions = []

        for sentence in hit["_source"]["sentences"]:
            offset = len(text_full)
            text_full += adjust_punctuation(sentence["text"]) + " "

            for claim in sentence["claim"]:
                start_pos = sentence["text"].find(claim)
                end_pos = start_pos + len(claim)
                arguments_positions.append({"type": "claim", "start": offset + start_pos, "end": offset + end_pos})

            for premise in sentence["premise"]:
                start_pos = sentence["text"].find(premise)
                end_pos = start_pos + len(premise)
                arguments_positions.append({"type": "premise", "start": offset + start_pos, "end": offset + end_pos})

            for entity in sentence["entities"]:
                type = entity["class"]
                text = entity["text"]
                start_pos = sentence["text"].find(text)
                end_pos = start_pos + len(text)
                entity_positions.append({"type": type, "start": offset + start_pos, "end": offset + end_pos})

        query_search_positions = []
        text_full_labeled = text_full
        for word in query_words:
            for match in set(re.findall(word, text_full_labeled, re.IGNORECASE)):
                positions = [{"start": m.start(), "end": m.end()} for m in re.finditer(match, text_full_labeled)]
                query_search_positions.extend(positions)

        doc["text_with_hit"] = adjust_punctuation(hit["highlight"]["sentences.text"][0])
        doc["text_full"] = text_full
        doc["text_full_labeled"] = text_full_labeled
        doc["query_positions"] = query_search_positions
        doc["arguments_positions"] = arguments_positions
        doc["entity_positions"] = entity_positions
        docs.append(doc)
    return json.dumps(docs)

def adjust_punctuation(text):
    return re.sub(r'\s([?.!,:;\'"](?:\s|$))', r'\1', text)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=6001, debug=False)

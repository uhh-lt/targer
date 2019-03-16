from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from util.Document import Document
from util.Sentence import Sentence
from util.data import parse_doc
from util.data import extract_arguments
from util.data import extract_entities
import re
import argparse


def delete_index(name):
    if es.indices.exists(name):
        print("deleting index for: '%s'" % (name))
        result = es.indices.delete(index=name)
        print(" result: '%s'" % (result))


def create_index(name):
    if not es.indices.exists(name):
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "document": {
                    "properties": {
                        "url": {"type": "text"},
                        "sentences": {
                            "type": "nested",
                            "properties": {
                                "text": {"type": "text"},
                                "claims": {
                                    "type": "nested",
                                    "properties": {
                                        "text": {"type": "text"},
                                        "score": {"type": "float"}
                                    }
                                },
                                "premises": {
                                    "type": "nested",
                                    "properties": {
                                        "text": {"type": "text"},
                                        "score": {"type": "float"}
                                    }
                                },
                                "entities": {
                                    "type": "nested",
                                    "properties": {
                                        "text": {"type": "text"},
                                        "class": {"type": "text"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        print("creating index for: '%s' " % (name))
        result = es.indices.create(index=name, body=request_body)
        print(" result: '%s'" % (result))

def parse_arguments(filename):
    docs = []

    with open(filename) as f:
        data = f.read()
        splt = data.split('# newdoc')
        for sp in splt:
            doc = parse_doc(sp)
            docs.append(doc)

    for doc in docs:
        if len(doc.sentences) == 0:
            continue

        currentDocument = {}
        sentences = []

        for sentence in doc.sentences:
            text, premise, claim = extract_arguments(sentence)
            currentSent = {}
            currentSent['text'] = text
            currentSent['claims'] = claim
            currentSent['premises'] = premise
            currentSent['entities'] = extract_entities(sentence)
            sentences.append(currentSent)

        currentDocument['_index'] = INDEX_NAME
        currentDocument['_type'] = "document"
        currentDocument['sentences']  = sentences
        currentDocument['url'] = re.search("(https?://[^\s]+)", doc.meta).group(0)
        yield currentDocument

parser = argparse.ArgumentParser(description='Index data')
parser.add_argument("-input", help="file to parse")
parser.add_argument("-host", help="host name")
parser.add_argument("-port", help="port", type=int)
args = parser.parse_args()

ES_SERVER = {"host": args.host, "port": args.port}
INDEX_NAME = 'arguments'

# init ES
es = Elasticsearch(hosts=[ES_SERVER])

#delete_index(INDEX_NAME)
create_index(INDEX_NAME)
bulk(es, parse_arguments(args.input))




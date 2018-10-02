from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from Document import Document
from Sentence import Sentence
import pandas as pd
import re

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
                                "claims": {"type": "text"},
                                "premises": {"type": "text"},
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

def parse_doc_from_raw(s):
    data = s
    paragraphs = data.split("\n\n")
    current_doc = Document()
    current_sentence = Sentence()
    for paragraph in paragraphs:
        if len(paragraph.strip()) == 0:
            continue
        # initial comment
        if paragraph.startswith("# parser"):
            break
        # new doc identifier
        if paragraph.strip().startswith("url ="):
            current_doc = Document()
            current_doc.meta = "# newdoc " + paragraph
            continue
        # sentence
        current_sentence = Sentence()
        words = paragraph.split("\n")
        for word in words:
            if len(word) > 0:
                if word.startswith("# sent_id"):
                    current_sentence.sent_id = word
                elif word.startswith("# text"):
                    current_sentence.text = word
                else:
                    current_sentence.add_word_conll(word)
        current_doc.add_sentence(current_sentence)
    return current_doc

def extract_arguments(sentence):
    sentence_text = " ".join([word.FORM for word in sentence.words_conll])
    sentence_claims = []
    sentence_premises = []

    prev = ""
    current_type = ""
    current_arg = []
    for word in sentence.words_conll:
        if word.ARGUMENT != prev and prev != "":
            if len(current_arg) > 0:
                if current_type == "P":
                    sentence_premises.append(" ".join(current_arg))
                if current_type == "C":
                    sentence_claims.append(" ".join(current_arg))
                current_arg = []

        if word.ARGUMENT != "O":
            current_arg.append(word.FORM)
            current_type = word.ARGUMENT
        prev = word.ARGUMENT

    if (len(current_arg) > 0):
        if current_type == "P":
            sentence_premises.append(" ".join(current_arg))
        if current_type == "C":
            sentence_claims.append(" ".join(current_arg))

    return sentence_text, sentence_premises, sentence_claims


def extract_entities(sentence):
    entities_result = []

    prev = ""
    current_type = ""
    current_entity = []
    for word in sentence.words_conll:
        if word.ENTITY != prev and prev != "":
            if len(current_entity) > 0:
                entity = {}
                entity['class'] = current_type
                entity['text'] = " ".join(current_entity)
                entities_result.append(entity)
                current_entity = []

        if word.ENTITY != "O":
            current_entity.append(word.FORM)
            current_type = word.ENTITY
        prev = word.ENTITY

    if (len(current_entity) > 0):
        entity = {}
        entity['class'] = current_type
        entity['text'] = " ".join(current_entity)
        entities_result.append(entity)

    return entities_result

def parse_arguments():
    docs = []
    with open('out_small.txt') as f:
        data = f.read()
        splt = data.split('# newdoc')
        for sp in splt:
            doc = parse_doc_from_raw(sp)
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
            currentSent['claim'] = claim
            currentSent['premise'] = premise
            currentSent['entities'] = extract_entities(sentence)
            sentences.append(currentSent)

        currentDocument['_index'] = INDEX_NAME
        currentDocument['_type'] = "document"
        currentDocument['sentences']  = sentences
        currentDocument['url'] = re.search("(https?://[^\s]+)", doc.meta).group(0)

        yield currentDocument

ES_SERVER = {"host": "localhost", "port": 9200}
INDEX_NAME = 'arguments'

# init ES
es = Elasticsearch(hosts=[ES_SERVER])

delete_index(INDEX_NAME)
create_index(INDEX_NAME)
bulk(es, parse_arguments())



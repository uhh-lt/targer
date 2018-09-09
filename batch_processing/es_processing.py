from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from Document import Document
from Sentence import Sentence

def extract_tokens(words_conll, pos):
    words = []
    for word in words_conll:
        if (len(word.strip()) > 0):
            words.append(word.split()[pos])
    return words

def parse_doc(s):
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
            if word.startswith("# sent_id"):
                current_sentence.sent_id = word
            elif word.startswith("# text"):
                current_sentence.text = word
            else:
                current_sentence.add_word_conll(word)
        current_doc.add_sentence(current_sentence)
    return current_doc


def parse_sentence(sentence):
    sentence_text = ""
    sentence_claim = ""
    sentence_premise = ""

    # get text
    words_list = extract_tokens(sentence.words_conll, 1)
    sentence_text = " ".join(words_list)

    # get arguments
    arguments_list = extract_tokens(sentence.words_conll, 9)
    for id, arg in enumerate(arguments_list):
        if arg == 'P-B' or arg == 'P-I':
            sentence_premise += words_list[id] + " "
        if arg == 'C-B' or arg == 'C-I':
            sentence_claim += words_list[id] + " "

    return sentence_text, sentence_premise, sentence_claim


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
            }
        }
        print("creating index for: '%s' " % (name))
        result = es.indices.create(index=name, body=request_body)
        print(" result: '%s'" % (result))

def parse_arguments():
    docs = []
    with open('out_small.txt') as f:
        data = f.read()
        splt = data.split('# newdoc')
        for sp in splt:
            doc = parse_doc(sp)
            docs.append(doc)

    for doc in docs:
        for sentence in doc.sentences:
            txt, pr, cl = parse_sentence(sentence)
            yield {
                "_index": INDEX_NAME,
                "_type": "argument",
                "text": txt, 
                "claim": cl, 
                "premise": pr
            }


ES_SERVER = {"host": "localhost", "port": 9200}
INDEX_NAME = 'arguments'

# init ES
es = Elasticsearch(hosts=[ES_SERVER])

#delete_index(INDEX_NAME)
create_index(INDEX_NAME)
bulk(es, parse_arguments())



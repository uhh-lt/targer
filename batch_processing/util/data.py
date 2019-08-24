from util.Document import Document
from util.Sentence import Sentence
from util.Word import Word
import numpy as np

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
            return None
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
    current_confidence = []
    for word in sentence.words_conll:
        if word.ARGUMENT != prev and prev != "":
            if len(current_arg) > 0:
                argument = {}
                argument['text'] = " ".join(current_arg)
                argument['score'] = np.round(np.mean(current_confidence), 2)
                if current_type == "P":
                    sentence_premises.append(argument)
                if current_type == "C":
                    sentence_claims.append(argument)
                current_arg = []
                current_confidence = []

        if word.ARGUMENT != "O":
            current_arg.append(word.FORM)
            current_confidence.append(word.CONFIDENCE)
            current_type = word.ARGUMENT
        prev = word.ARGUMENT

    if (len(current_arg) > 0):
        argument = {}
        argument['text'] = " ".join(current_arg)
        argument['score'] = np.round(np.mean(current_confidence), 2)
        if current_type == "P":
            sentence_premises.append(argument)
        if current_type == "C":
            sentence_claims.append(argument)

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

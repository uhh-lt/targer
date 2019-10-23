import re
import json
import sys

SEARCH_KEY_PREMISE = 'premise'
SEARCH_KEY_CLAIM = 'claim'
SEARCH_KEY_ENTITY = 'named_entity'
SEARCH_KEY_TEXT = 'text'

def search_in_es(es, index_name, query, where_to_seach, confidence):
    number_of_sentences_around = 3
    docs = []
    search_query = query[:100]

    search_elements = []
    for search_category in where_to_seach:
        if search_category == SEARCH_KEY_TEXT:
            search_elements.append(get_search_field("sentences", "sentences.text", search_query))
        if search_category == SEARCH_KEY_PREMISE:
            search_elements.append(
                get_search_field_with_score("sentences.premises", "sentences.premises.text", search_query,
                                            "sentences.premises.score", float(confidence) / 100))
        if search_category == SEARCH_KEY_CLAIM:
            search_elements.append(
                get_search_field_with_score("sentences.claims", "sentences.claims.text", search_query,
                                            "sentences.claims.score", float(confidence) / 100))
        if search_category == SEARCH_KEY_ENTITY:
            search_elements.append(get_search_field("sentences.entities", "sentences.entities.text", search_query))

    if len(search_elements) == 0:
        search_elements.append(get_search_field("sentences", "sentences.text", search_query))

    res = es.search(index=index_name, request_timeout=60, body={"from": 0, "size": 25,

                                                                "query": {
                                                                    "bool": {
                                                                        "should": search_elements
                                                                    }
                                                                }})

    query_words = search_query.strip().split()
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        try:
            doc = {}
            text_full = ""
            arguments_positions = []
            entity_positions = []
            query_search_positions = []

            sentences = hit["_source"]["sentences"]

            field = "sentences"
            if SEARCH_KEY_PREMISE in where_to_seach and hit["inner_hits"]["sentences.premises"]["hits"]["total"] > 0:
                field = "sentences.premises"
            elif SEARCH_KEY_CLAIM in where_to_seach and hit["inner_hits"]["sentences.claims"]["hits"]["total"] > 0:
                field = "sentences.claims"
            elif SEARCH_KEY_ENTITY in where_to_seach and hit["inner_hits"]["sentences.entities"]["hits"]["total"] > 0:
                field = "sentences.entities"

            index_with_top_match = hit["inner_hits"][field]["hits"]["hits"][0]["_nested"]["offset"]

            # finding for sentences indexes to show
            if len(sentences) < 7:
                min_pos = 0
                max_pos = len(sentences) - 1
            elif index_with_top_match < number_of_sentences_around:
                min_pos = 0
                max_pos = number_of_sentences_around * 2
            elif index_with_top_match > (len(sentences) - (number_of_sentences_around * 2 + 2)):
                min_pos = (len(sentences) - (number_of_sentences_around * 2 + 2))
                max_pos = (len(sentences) - 1)
            else:
                min_pos = index_with_top_match - number_of_sentences_around
                max_pos = index_with_top_match + number_of_sentences_around

            for sentence_index in range(min_pos, max_pos + 1):

                sentence = sentences[sentence_index]
                offset = len(text_full)
                sentence_text_adjusted = adjust_punctuation(sentence['text'])
                text_full += sentence_text_adjusted + " "

                # finding positions for claims
                if SEARCH_KEY_CLAIM in where_to_seach:
                    for claim in sentence["claims"]:
                        if (float(claim["score"]) > float(confidence) / 100):
                            claim_adjusted = adjust_punctuation(claim["text"])
                            start_pos = sentence_text_adjusted.find(claim_adjusted)
                            end_pos = start_pos + len(claim_adjusted)
                            arguments_positions.append(
                                {"type": "claim", "start": offset + start_pos, "end": offset + end_pos})

                # finding positions for premises
                if SEARCH_KEY_PREMISE in where_to_seach:
                    for premise in sentence["premises"]:
                        if (float(premise["score"]) > float(confidence) / 100):
                            premise_adjusted = adjust_punctuation(premise["text"])
                            start_pos = sentence_text_adjusted.find(premise_adjusted)
                            end_pos = start_pos + len(premise_adjusted)
                            arguments_positions.append(
                                {"type": "premise", "start": offset + start_pos, "end": offset + end_pos})

                # finding positions for entities
                if SEARCH_KEY_ENTITY in where_to_seach:
                    for entity in sentence["entities"]:
                        if entity["class"].upper() == "ORGANIZATION":
                            type = "ORG"
                        elif entity["class"].upper() == "LOCATION":
                            type = "LOC"
                        else:
                            type = entity["class"]
                        text = adjust_punctuation(entity["text"])
                        start_pos = sentence_text_adjusted.find(text)
                        end_pos = start_pos + len(text)
                        entity_positions.append({"type": type, "start": offset + start_pos, "end": offset + end_pos})

            # finding positions for search query instances
            for word in query_words:
                for match in set(re.findall(word, text_full, re.IGNORECASE)):
                    positions = [{"type": "search", "start": m.start(), "end": m.end()} for m in
                                 re.finditer(match, text_full)]
                    query_search_positions.extend(positions)

            doc["text_full"] = text_full
            doc["query_positions"] = query_search_positions
            doc["arguments_positions"] = arguments_positions
            doc["entity_positions"] = entity_positions
            doc["url"] = hit["_source"]["url"]
            docs.append(doc)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    return json.dumps(docs)

def get_search_field(path, field, query):
    return {"nested": {
        "path": path,
        "query": {
            "bool": {
                "must": [{"match": {field: {"query": query}}}]
            }
        },
        "inner_hits": {}
    }}


def get_search_field_with_score(path, field, query, score_field, score):
    return {"nested": {
        "path": path,
        "query": {
            "bool": {
                "must": [{"match": {field: {"query": query}}},
                         {"range": {score_field: {"gt": score}}}]
            }
        },
        "inner_hits": {}
    }}


def adjust_punctuation(text):
    return re.sub(r'\s([?.!,:;\'"](?:\s|$))', r'\1', text)
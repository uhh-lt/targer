import sys
sys.path.insert(0, "./lstm")

from lstm.src.factories.factory_tagger import TaggerFactory

import nltk
import json

path = "models/model_new_es.hdf5"

def replace_labels(input):
    return input.replace('B-Premise','P-B').replace('I-Premise','P-I').replace('I-Claim','C-I').replace('B-Claim','C-B').replace("B-MajorClaim", "C-B").replace("I-MajorClaim", "C-I")

class ModelNewES:

    tagger =TaggerFactory.load(path, -1)

    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def label(self, input):
        sentences = [ nltk.word_tokenize(input) ]

        output = self.tagger.predict_tags_from_words(sentences, batch_size=200)

        output = [[replace_labels(t) for t in s] for s in output]

        result = []
        for sentenceIdx in range(len(sentences)):
            tokens = sentences[sentenceIdx]
            sentence = []
            for tokenIdx in range(len(tokens)):
                currentWord = {}
                currentWord['token'] = tokens[tokenIdx]
                currentWord['label'] = output[sentenceIdx][tokenIdx]
                sentence.append(currentWord)
            result.append(sentence)

        return result

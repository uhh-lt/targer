import sys
sys.path.insert(0, "./lstm")

from lstm.src.factories.factory_tagger import TaggerFactory

import nltk
import json

path = "models/model_new_wd.hdf5"


class ModelNewWD:

    tagger =TaggerFactory.load(path, -1)

    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def label(self, input):
        sentences = [ nltk.word_tokenize(input) ]

        output = self.tagger.predict_tags_from_words(sentences, batch_size=200)

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

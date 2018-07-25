from __future__ import print_function
import nltk
from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM
import sys
import json


modelPath = "models/ES_k.h5"

class ModelESk:

    lstmModel = BiLSTM.loadModel(modelPath)

    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def label(self, input):
        #prepare input
        sentences = [{'tokens': nltk.word_tokenize(sent)} for sent in nltk.sent_tokenize(input)]
        addCharInformation(sentences)
        addCasingInformation(sentences)
        dataMatrix = createMatrices(sentences, self.lstmModel.mappings, True)

        #tag input
        tags = self.lstmModel.tagSentences(dataMatrix)

        #prepare output
        result = []
        for sentenceIdx in range(len(sentences)):
            tokens = sentences[sentenceIdx]['tokens']
            sentence = []
            for tokenIdx in range(len(tokens)):
                tokenTags = []
                currentWord = {}
                for modelName in sorted(tags.keys()):
                    tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])
        
                currentWord['token'] = tokens[tokenIdx]
                currentWord['label'] = tokenTags[0]
                sentence.append(currentWord)
            result.append(sentence)

        return json.dumps(result)

    def label_with_probs(self, input):
        #prepare input
        sentences = [{'tokens': nltk.word_tokenize(sent)} for sent in nltk.sent_tokenize(input)]
        addCharInformation(sentences)
        addCasingInformation(sentences)
        dataMatrix = createMatrices(sentences, self.lstmModel.mappings, True)

        #tag input
        tags, probs = self.lstmModel.tagSentences_with_probs(dataMatrix)

        #prepare output
        result = []
        for sentenceIdx in range(len(sentences)):
            tokens = sentences[sentenceIdx]['tokens']
            sentence = []
            for tokenIdx in range(len(tokens)):
                tokenTags = []
                probTags = []
                currentWord = {}
                for modelName in sorted(tags.keys()):
                    tokenTags.append(tags[modelName][sentenceIdx][tokenIdx])
                    probTags.append(probs[modelName][sentenceIdx][tokenIdx])

                currentWord['token'] = tokens[tokenIdx]
                currentWord['label'] = tokenTags[0]
                currentWord['prob'] = probTags[0]
                sentence.append(currentWord)
            result.append(sentence)

        return result

#example usage
#text = "Therefore fixed punishment will decrease the space between poor and rich people and everyone will understand the importance of each other. Yes I will."
#model = Model()
#print(model.label(text))
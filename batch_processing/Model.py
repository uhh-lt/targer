from __future__ import print_function
import nltk
from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM

class Model:

    lstmModel = None

    def __init__(self, path):
        print("Init Model")
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        if (self.lstmModel is None):
            self.lstmModel = BiLSTM.loadModel(path)

    def label_structured_with_probs(self, input):
        #prepare input
        sentences = input
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
                    #print(probs[modelName][sentenceIdx][tokenIdx])
                    probTags.append(probs[modelName][sentenceIdx][tokenIdx])

                currentWord['token'] = tokens[tokenIdx]
                currentWord['label'] = tokenTags[0]
                currentWord['prob'] = probTags[0]
                sentence.append(currentWord)
            result.append(sentence)

        return result

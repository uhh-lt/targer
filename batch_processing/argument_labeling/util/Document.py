class Document:

    def __init__(self):
        self.meta = ""
        self.sentences = []

    def add_sentence(self, sentence):
        self.sentences.append(sentence)
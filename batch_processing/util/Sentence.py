from util.Word import Word

class Sentence:

    def __init__(self):
        self.sent_id = ""
        self.text = ""
        self.words_conll = []

    def add_word_conll(self, word):
        self.words_conll.append(Word(word))

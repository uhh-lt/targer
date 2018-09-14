class Word:

    def __init__(self, text):
        fields = text.split()
        self.id = fields[0]
        self.FORM = fields[1]
        self.LEMMA = fields[2]
        self.UPOS = fields[3]
        self.XPOS = fields[4]
        self.HEAD = fields[5]
        self.DEPREL = fields[6]
        self.DEPS = fields[7]
        self.ENTITY = fields[8]
        self.ARGUMENT = fields[9]

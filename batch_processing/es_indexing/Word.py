class Word:

    def __init__(self, text):
        fields = text.split()
        self.FORM = fields[1]
        self.ENTITY = fields[8].replace("B-", "").replace("I-", "")
        self.ARGUMENT = fields[9].replace("-B", "").replace("-I", "")

class Word:

    def __init__(self, text):
        fields = text.split("\t")
        self.ID = int(fields[0])
        self.FORM = fields[1]
        self.LEMMA = fields[2]
        self.UPOSTAG = fields[3]
        self.XPOSTAG = fields[4]
        self.HEAD = fields[5]
        self.DEPREL = fields[6]
        self.DEPS = fields[7]

        self.ENTITY = fields[8].replace("B-", "").replace("I-", "")

        if len(fields) > 9:
            self.ARGUMENT = fields[9].replace("-B", "").replace("-I", "")
        else:
            self.ARGUMENT = "_"

        if len(fields) > 10:
            self.CONFIDENCE = float(fields[10])
        else:
            self.CONFIDENCE = -1

    def get_CONLL_row(self):
        fields = []
        fields.append(str(self.ID))
        fields.append(self.FORM)
        fields.append(self.LEMMA)
        fields.append(self.UPOSTAG)
        fields.append(self.XPOSTAG)
        fields.append(self.HEAD)
        fields.append(self.DEPREL)
        fields.append(self.DEPS)
        fields.append(self.ENTITY)

        if (self.ARGUMENT != "_"):
            fields.append(self.ARGUMENT)

        if (self.CONFIDENCE != -1):
            fields.append(str(self.CONFIDENCE))

        return "\t".join(fields)

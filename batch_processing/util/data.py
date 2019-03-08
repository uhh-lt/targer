from util.Document import Document
from util.Sentence import Sentence
from util.Word import Word

def parse_doc(s):
    data = s
    paragraphs = data.split("\n\n")
    current_doc = Document()
    current_sentence = Sentence()
    for paragraph in paragraphs:
        if len(paragraph.strip()) == 0:
            continue
        # initial comment
        if paragraph.startswith("# parser"):
            return None
        # new doc identifier
        if paragraph.strip().startswith("url ="):
            current_doc = Document()
            current_doc.meta = "# newdoc " + paragraph
            continue
        # sentence
        current_sentence = Sentence()
        words = paragraph.split("\n")
        for word in words:
            if len(word) > 0:
                if word.startswith("# sent_id"):
                    current_sentence.sent_id = word
                elif word.startswith("# text"):
                    current_sentence.text = word
                else:
                    current_sentence.add_word_conll(word)
        current_doc.add_sentence(current_sentence)
    return current_doc
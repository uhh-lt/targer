from multiprocessing import Pool
from Model import Model
from Document import Document
from Sentence import Sentence
import time

def extract_tokens(words_conll):
    words = ""
    for word in words_conll:
        if (len(word.strip()) > 0):
            words+=word.split()[1]
            words+=" "
    return words

def label_doc(document):
    doc_raw_text = ""
    doc_output = document.meta + "\n"
    for sentence in document.sentences:
        extracted = extract_tokens(sentence.words_conll)
        doc_raw_text += extracted
    labeled_doc = model.label(doc_raw_text)
    sentence_index = 0
    for sentence in document.sentences:
        labeled_sentence = labeled_doc[sentence_index]
        sentence_index += 1
        doc_output += "\n" + sentence.sent_id + "\n"
        doc_output += sentence.text + "\n"
        word_index = 0
        for word in sentence.words_conll:
            try:
                dictionary = labeled_sentence[word_index]
                doc_output+=word + "\t" + dictionary["label"] + "\n"
                word_index += 1
            except IndexError:
                #print ("error")
                pass
    return doc_output

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
            break
        # new doc identifier
        if paragraph.strip().startswith("url ="):
            current_doc = Document()
            current_doc.meta = "# newdoc " + paragraph
            continue
        # sentence
        current_sentence = Sentence()
        words = paragraph.split("\n")
        for word in words:
            if word.startswith("# sent_id"):
                current_sentence.sent_id = word
            elif word.startswith("# text"):
                current_sentence.text = word
            else:
                current_sentence.add_word_conll(word)
        current_doc.add_sentence(current_sentence)
    return current_doc

def initializer():
    global model
    st = time.time()
    model = Model()
    print("model loaded: ", time.time() - st)

def write(text):
    with open("out.txt", "a") as myfile:
        myfile.write("\n")
        myfile.write(text)

model = None

if __name__ == '__main__':
    time_start = time.time()
    with open("out.txt", "w") as myfile:
        myfile.write("")

    texts_to_label = []
    with open('xaa') as f:  
        data = f.read()  
        splt = data.split('# newdoc')  
        for sp in splt:
            doc = parse_doc(sp)
            texts_to_label.append(doc)

    with Pool(6, initializer, ()) as p:
        for result in p.map(label_doc,  texts_to_label):
            write(result)

    print(time.time() - time_start)

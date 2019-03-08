from multiprocessing import Pool
from Model import Model
from util.Document import Document
from util.Sentence import Sentence
from util.Word import Word
from util.data import parse_doc
import time
import argparse

def label_doc(document):
    sentences_to_process = []
    doc_output = document.meta + "\n"
    for sentence in document.sentences:
        tokens = [word.FORM for word in sentence.words_conll]
        sentences_to_process.append({'tokens': tokens})

    labeled_doc = model.label_structured_with_probs(sentences_to_process)

    for sentence_index, sentence in enumerate(document.sentences):
        labeled_sentence = labeled_doc[sentence_index]
        doc_output += "\n" + sentence.sent_id + "\n"
        doc_output += sentence.text + "\n"
        for word_index, word in enumerate(sentence.words_conll):
            try:
                dictionary = labeled_sentence[word_index]
                word.ARGUMENT = dictionary["label"]
                word.CONFIDENCE = dictionary["prob"]
                doc_output += word.get_CONLL_row() + "\n"
            except Exception as e:
                print(e)
                pass
    return doc_output


def initializer(path):
    global model
    start_time = time.time()
    model = Model(path)
    print("model loaded in ", time.time() - start_time)

def write(text, filename):
    with open(filename, "a") as myfile:
        myfile.write("\n")
        myfile.write(text)


if __name__ == '__main__':
    time_start = time.time()

    parser = argparse.ArgumentParser(description='Argument labeling')
    parser.add_argument('--input',
                        required=True,
                        help='input data',
                        default='input')
    parser.add_argument('--model',
                        required=True,
                        help='model to use',
                        default='model.h5')
    parser.add_argument('--output',
                        required=True,
                        help='labeled data',
                        default='output')
    parser.add_argument('--workers',
                        type=int,
                        required=False,
                        help='labeled data',
                        default=1)
    args = parser.parse_args()


    with open(args.output, "w") as myfile:
        myfile.write("")

    texts_to_label = []
    with open(args.input) as f:
        data = f.read()  
        splt = data.split('# newdoc')
        for sp in splt:
            if len(sp.strip()) > 0:
                doc = parse_doc(sp)
                if doc != None:
                    texts_to_label.append(doc)

    with Pool(processes = args.workers, initializer = initializer, initargs = [args.model]) as p:
        for result in p.map(label_doc,  texts_to_label):
            write(result, args.output)

    print("Time: ", time.time() - time_start)

import datetime
from pyspark import SparkContext, SparkConf
import json
from Document import Document
from Sentence import Sentence

from Model import Model
model = Model()

def parse_doc(s):
    _, data = s
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
        # alternatively use text provided in data set 
        # doc_raw_text += sentence.text[]
    labeled_doc = model.label(doc_raw_text)
    sentence_index = 0
    for sentence in document.sentences:
        labeled_sentence = labeled_doc[sentence_index]
        sentence_index += 1

        doc_output += "\n" + sentence.sent_id + "\n"
        doc_output += sentence.text + "\n"
        word_index = 0
        for word in sentence.words_conll:
            dictionary = labeled_sentence[word_index]
            doc_output+=word + "\t" + dictionary["label"] + "\n"
            word_index += 1
    return doc_output

conf = SparkConf().setAppName('rnn2argument')
sc = SparkContext(conf=conf)
print("available nodes: ", sc.defaultParallelism)

text = sc.newAPIHadoopFile(
    "conll.txt",
    'org.apache.hadoop.mapreduce.lib.input.TextInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'org.apache.hadoop.io.Text',
    conf={'textinputformat.record.delimiter': '# newdoc'}
)

text.map(lambda x: parse_doc(x))\
    .map(lambda x: label_doc(x)) \
    .saveAsTextFile("output")

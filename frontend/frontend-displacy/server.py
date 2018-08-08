from flask import Flask, render_template
from json import JSONDecodeError
import requests
import json
from flask import request

app = Flask(__name__)

class Sender:
    def send(self, text, classifier):
        
        if classifier == "WD":
            url = "http://ltdemos.informatik.uni-hamburg.de/arg-mining-ltcpu/classifyWD"
        elif classifier == "WD_dep":
            url = "http://ltdemos.informatik.uni-hamburg.de/arg-mining-ltcpu/classifyWD_dep"
        elif classifier == "ES":
            url = "http://ltdemos.informatik.uni-hamburg.de/arg-mining-ltcpu/classifyES"
        elif classifier == "ES_dep":
            url = "http://ltdemos.informatik.uni-hamburg.de/arg-mining-ltcpu/classifyES_dep"
        elif classifier == "IBM":
            url = "http://ltdemos.informatik.uni-hamburg.de/arg-mining-ltcpu/classifyIBM"
        
        try:
            r = requests.post(url, data=text.encode("utf-8"))
            return r.json()
        except JSONDecodeError:
            print("!!!!", len(text), text)
            pass

sender = Sender()

@app.route('/')
def index():
  return render_template('displacy.html')

@app.route('/label_text', methods=['POST'])
def background_process_test():
    text = request.form.get('username')
    classifier = request.form.get('classifier')
    doc = sender.send(text, classifier)
    currentPos = 0
    data = []
    for sentence in doc:
        for token in sentence:
            start = text.find(token["token"], currentPos)
            end = start + len(token["token"])
            currentPos = end
            currentWord = {}
            currentWord['start'] = start
            currentWord['end'] = end
            currentWord['type'] = token["label"]
            data.append(currentWord)
    return json.dumps(data)

if __name__ == '__main__':
  app.run(debug=True)



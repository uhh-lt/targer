from flask import Flask, render_template
from json import JSONDecodeError
import requests
import json
import urllib.parse
import urllib.request as req
from flask import request

app = Flask(__name__)

class Sender:
    def send(self, text):
        try:
            r = requests.post("http://ltdemos.informatik.uni-hamburg.de/arg-mining-ltcpu/classifyES", data=text.encode("utf-8"))
            return r.json()
        except JSONDecodeError:
            print("!!!!", len(text), text)
            pass

sender = Sender()

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/label_text')
def background_process_test():
    text = request.args.get('username')
    print ("Hello, ", text)
    doc = sender.send(text)
    print(doc)
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


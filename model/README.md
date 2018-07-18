# Model usage

How to use:

1. Cloning the following repo:
https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf

2. Replace their BiLSTM.py with file from this repo (extended with method to get confidence score for prediction).

3. Downloading the pretrained model.

    * ES dataset with "shrinked" fasttext embeddings: https://goo.gl/LJ25ze
    * WD dataset with "shrinked" fasttext embeddings: https://goo.gl/H1xKg9
    * ES dataset with full Dependency Based embeddings by [1]: https://goo.gl/gcF8VP
    * WD dataset with full  Dependency Based embeddings by [1]:  https://goo.gl/82iWwA

4. Using Model class in Model.py to run pretrained model on a new input:

Labeling:

```python
text = "Therefore fixed punishment will decrease the space between poor and rich people and everyone will understand the importance of each other. Yes I will."
model = Model()
print(model.label(text))

[[{"token": "Therefore", "label": "O"}, {"token": "fixed", "label": "C-B"}, {"token": "punishment", "label": "C-I"}, {"token": "will", "label": "C-I"}, {"token": "decrease", "label": "C-I"}, {"token": "the", "label": "C-I"}, {"token": "space", "label": "C-I"}, {"token": "between", "label": "C-I"}, {"token": "poor", "label": "C-I"}, {"token": "and", "label": "C-I"}, {"token": "rich", "label": "C-I"}, {"token": "people", "label": "C-I"}, {"token": "and", "label": "C-I"}, {"token": "everyone", "label": "C-I"}, {"token": "will", "label": "C-I"}, {"token": "understand", "label": "C-I"}, {"token": "the", "label": "C-I"}, {"token": "importance", "label": "C-I"}, {"token": "of", "label": "C-I"}, {"token": "each", "label": "C-I"}, {"token": "other", "label": "C-I"}, {"token": ".", "label": "O"}], [{"token": "Yes", "label": "O"}, {"token": "I", "label": "O"}, {"token": "will", "label": "O"}, {"token": ".", "label": "O"}]]
```

Labeling and confidence score:

```python
text = "Therefore fixed punishment will decrease the space between poor and rich people and everyone will understand the importance of each other. Yes I will."
model = Model()
print(model.label_with_probs(text))

[[{'label': 'O', 'prob': '0.9248742', 'token': 'Therefore'}, {'label': 'C-B', 'prob': '0.44421706', 'token': 'fixed'}, {'label': 'C-I', 'prob': '0.4107555', 'token': 'punishment'}, {'label': 'C-I', 'prob': '0.49298504', 'token': 'will'}, {'label': 'C-I', 'prob': '0.48158503', 'token': 'decrease'}, {'label': 'C-I', 'prob': '0.47499213', 'token': 'the'}, {'label': 'C-I', 'prob': '0.46752247', 'token': 'space'}, {'label': 'C-I', 'prob': '0.44668216', 'token': 'between'}, {'label': 'C-I', 'prob': '0.43725127', 'token': 'poor'}, {'label': 'C-I', 'prob': '0.41270158', 'token': 'and'}, {'label': 'C-I', 'prob': '0.39943892', 'token': 'rich'}, {'label': 'C-I', 'prob': '0.38194695', 'token': 'people'}, {'label': 'C-I', 'prob': '0.3775853', 'token': 'and'}, {'label': 'C-I', 'prob': '0.35318276', 'token': 'everyone'}, {'label': 'C-I', 'prob': '0.3679205', 'token': 'will'}, {'label': 'C-I', 'prob': '0.34831274', 'token': 'understand'}, {'label': 'C-I', 'prob': '0.3565875', 'token': 'the'}, {'label': 'C-I', 'prob': '0.36702344', 'token': 'importance'}, {'label': 'P-I', 'prob': '0.34357774', 'token': 'of'}, {'label': 'P-I', 'prob': '0.33412224', 'token': 'each'}, {'label': 'P-I', 'prob': '0.33728018', 'token': 'other'}, {'label': 'O', 'prob': '0.99704343', 'token': '.'}], [{'label': 'O', 'prob': '0.95338166', 'token': 'Yes'}, {'label': 'O', 'prob': '0.986553', 'token': 'I'}, {'label': 'O', 'prob': '0.9626477', 'token': 'will'}, {'label': 'O', 'prob': '0.99946254', 'token': '.'}]]
```

[1] Alexandros Komninos and Suresh Manandhar. 2016. Dependency Based Embeddings for Sentence Classification Tasks. In Proceedings of NAACL

# Model usage

How to use:

1. Cloning the following repo:
https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf

2. Downloading the pretrained model. https://goo.gl/5cFJWT (old)

Trained on:

ES dataset with "shrinked" fasttext embeddings: https://goo.gl/heAHLb
WD dataset with "shrinked" fasttext embeddings: https://goo.gl/7CAotT

ES dataset with full Dependency Based embeddings by [1]: https://goo.gl/WZgsiE
WD dataset with full  Dependency Based embeddings by [1]:  https://goo.gl/nvtqrY

3. Using Model class in Model.py to run pretrained model on a new input:


```python
text = "Therefore fixed punishment will decrease the space between poor and rich people and everyone will understand the importance of each other. Yes I will."
model = Model()
print(model.label(text))

[[{"token": "Therefore", "label": "O"}, {"token": "fixed", "label": "C-B"}, {"token": "punishment", "label": "C-I"}, {"token": "will", "label": "C-I"}, {"token": "decrease", "label": "C-I"}, {"token": "the", "label": "C-I"}, {"token": "space", "label": "C-I"}, {"token": "between", "label": "C-I"}, {"token": "poor", "label": "C-I"}, {"token": "and", "label": "C-I"}, {"token": "rich", "label": "C-I"}, {"token": "people", "label": "C-I"}, {"token": "and", "label": "C-I"}, {"token": "everyone", "label": "C-I"}, {"token": "will", "label": "C-I"}, {"token": "understand", "label": "C-I"}, {"token": "the", "label": "C-I"}, {"token": "importance", "label": "C-I"}, {"token": "of", "label": "C-I"}, {"token": "each", "label": "C-I"}, {"token": "other", "label": "C-I"}, {"token": ".", "label": "O"}], [{"token": "Yes", "label": "O"}, {"token": "I", "label": "O"}, {"token": "will", "label": "O"}, {"token": ".", "label": "O"}]]
```
[1] Alexandros Komninos and Suresh Manandhar. 2016. Dependency Based Embeddings for Sentence Classification Tasks. In Proceedings of NAACL

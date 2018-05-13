# Model usage

How to use:

1. Cloning the following repo:
https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf

2. Downloading the pretrained model. (link coming soon)

3. Using Model class in Model.py to run pretrained model on a new input:


```python
text = "Therefore fixed punishment will decrease the space between poor and rich people and everyone will understand the importance of each other."
model = Model()
print(model.label(text))
```

# Argument labeling

Script parses the conll file with argument labels and saves to ES index. 


#### example of input data:
```
# sent_id = http://www.usingenglish.com/profiles/tdol/archives/000265.html#2
# text = The more I looked at this sentence, the crasser it appeared to me.
0       The     the     DT      DT              1       dep     1:dep   O       P-B
1       more    more    JJR     JJR             3       advmod  3:advmod        O       P-I
2       I       I       PRP     PRP             3       nsubj   3:nsubj O       P-I
3       looked  look    VBD     VBD             3       ROOT    3:ROOT  O       P-I
4       at      at      IN      IN              3       prep    _       O       P-I
5       this    this    DT      DT              6       det     6:det   O       P-I
6       sentence        sentence        NN      NN              4       pobj    3:prep_at       O       P-I
7       ,       ,       ,       ,               3       punct   3:punct O       P-I
8       the     the     DT      DT              9       det     9:det   O       P-I
9       crasser crasser NN      NN              7       dobj    7:dobj  O       P-I
10      it      it      PRP     PRP             11      nsubj   11:nsubj        O       P-I
11      appeared        appear  VBD     VBD             9       rcmod   9:rcmod O       P-I
12      to      to      TO      TO              11      prep    _       O       P-I
13      me      I       PRP     PRP             12      pobj    11:prep_to      O       P-I
14      .       .       .       .               3       punct   3:punct O       O

```

#### example of ES document:

```
{
  "_index": "arguments",
  "_type": "document",
  "_id": "6rXU02UBG3chk-754ccv",
  "_score": 1,
  "_source": {
    "sentences": [
      {
        "claim": [],
        "entities": [
          {
            "text": "Sangla Valley",
            "class": "Location"
          }
        ],
        "text": "Sangla Valley in Himachal Pradesh in India .",
        "premise": [
          "Sangla Valley in Himachal Pradesh in India"
        ]
      },
      {
        "claim": [],
        "entities": [
          {
            "text": "Samgla",
            "class": "Person"
          }
        ],
        "text": "Samgla is the best for the Apple .",
        "premise": [
          "Samgla is the best for the Apple"
        ]
      }
    ],
    "url": "http://attractivespot.blogspot.com/2012/03/sangla-vallay-in-himachal-in-india.html"
  }
}
```
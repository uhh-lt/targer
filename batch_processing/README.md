# Argument labeling


For labeling script label_mp.py is used. It takes such a parameters:

```
--input # input filename
--model # model to use for labelling
--output # output filename
--workers # number of CPUs to use
```
Script takes text file in a CONLL format as an input. Then  parse out the sentence, applies model to it to label with arguments. Argument labels and confidence scores are added as an additional fields(columns) in a conll file. 


#### example of input data:
```
# newdoc        url = http://attractivespot.blogspot.com/2012/03/sangla-vallay-in-himachal-in-india.html        s3 = s3://aws-publicdatasets/common-crawl/crawl-data/CC-MAIN-2016-07/segments/1454701152130.53/warc/CC-MAIN-20160205193912-00334-ip-10-236-182-209.ec2.internal.warc.gz

# sent_id = http://attractivespot.blogspot.com/2012/03/sangla-vallay-in-himachal-in-india.html#1
# text = Sangla Valley in Himachal Pradesh in India .
0       Sangla  Sangla  NNP     NNP             1       nn      1:nn    B-Location
1       Valley  Valley  NNP     NNP             1       ROOT    1:ROOT  I-Location
2       in      in      IN      IN              1       prep    _       O
3       Himachal        Himachal        NNP     NNP             4       nn      4:nn    O
4       Pradesh Pradesh NNP     NNP             2       pobj    1:prep_in       O
5       in      in      IN      IN              1       prep    _       O
6       India   India   NNP     NNP             5       pobj    1:prep_in       O
7       .       .       .       .               1       punct   1:punct O
```

#### example of output:

```
# sent_id = http://www.usingenglish.com/profiles/tdol/archives/000265.html#2
# text = The more I looked at this sentence, the crasser it appeared to me.
0       The     the     DT      DT              1       dep     1:dep   O       P-B   0.97
1       more    more    JJR     JJR             3       advmod  3:advmod        O       P-I   0.90
2       I       I       PRP     PRP             3       nsubj   3:nsubj O       P-I   0.91
3       looked  look    VBD     VBD             3       ROOT    3:ROOT  O       P-I   0.95
4       at      at      IN      IN              3       prep    _       O       P-I   0.95
5       this    this    DT      DT              6       det     6:det   O       P-I   0.99
6       sentence        sentence        NN      NN              4       pobj    3:prep_at       O       P-I   0.89
7       ,       ,       ,       ,               3       punct   3:punct O       P-I   0.93
8       the     the     DT      DT              9       det     9:det   O       P-I   0.94
9       crasser crasser NN      NN              7       dobj    7:dobj  O       P-I   0.94
10      it      it      PRP     PRP             11      nsubj   11:nsubj        O       P-I   0.85
11      appeared        appear  VBD     VBD             9       rcmod   9:rcmod O       P-I   0.74
12      to      to      TO      TO              11      prep    _       O       P-I   0.75
13      me      I       PRP     PRP             12      pobj    11:prep_to      O       P-I   0.73
14      .       .       .       .               3       punct   3:punct O       O   0.99

```

# ES indexing


For indexing script index.py is used. It takes such a parameters:

```
--input # input filename
--host # host name of Elastic Search server
--port # port number of Elastic Search server
```

Script parses the conll file with argument labels and saves to ES index. 

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
        "claims": [],
        "entities": [
          {
            "text": "Sangla Valley",
            "class": "Location"
          }
        ],
        "text": "Sangla Valley in Himachal Pradesh in India .",
        "premises": [
          {
            "text": "Sangla Valley in Himachal Pradesh in India",
            "score": 97.33
          }
        ]
      },
      {
        "claims": [],
        "entities": [
          {
            "text": "Samgla",
            "class": "Person"
          }
        ],
        "text": "Samgla is the best for the Apple .",
        "premises": [
          {
            "text": "Samgla is the best for the Apple",
            "score": 97.33
          }
        ]
      }
    ],
    "url": "http://attractivespot.blogspot.com/2012/03/sangla-vallay-in-himachal-in-india.html"
  }
}
```

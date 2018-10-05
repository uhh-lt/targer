# Argument labeling




Script takes text file in a CONLL format as an input. Then  parse out the sentence, applies model to it to label with arguments. Argument labels are added as an additional field(column) in a conll file. 


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
##############################################
# Python script showing how many triples     #
# we have by annotator (with some details)   #
# like how many with dates, coreference, etc #
##############################################

import os
import json
import argparse
import pandas as pd

annotator_nosub = "NoSubject-Triple-aligner"
annotator_simple = "Simple-Aligner"
annotator_SPO = "SPOAligner"
annotator_NosubSPO = "NosubSPOAligner"


parser = argparse.ArgumentParser(description='filter extracted attributes')
parser.add_argument('-i', '--input', help='input folder name', required=True)
parser.add_argument('-o', '--out', help='input file name', required=True)
args = parser.parse_args()

# [text, triple1 , ... triple 10, annotator]
data = []

for file in os.listdir(args.input):
     with open(os.path.join(args.input, file)) as f:
         j = json.load(f)
         for d in j:

             # iterate over every document

             t = [x for x in d['triples'] if annotator_NosubSPO in x['annotator']]

             text = ""
             if len(t) > 2:

                 row = []

                 maxsent = 0

                 for c, x in enumerate(t):

                     if x['sentence_id'] > maxsent:

                         maxsent = x['sentence_id']

                     row.append(d['title'] + "\t" + x['predicate']['surfaceform'] + "\t" + x['object']['surfaceform'])
                     text = d['text'][0:d['sentences_boundaries'][maxsent][1]]


                 row = list(set(row))

                 if len(row) > 10:
                     row = row[0:10]

                 elif len(row) < 10:
                     row += [None] * (10 - len(row))

                 row = [text] + row
                 row += [x['annotator']]

                 data.append(row)


names = ["Original Sentence"]

for i in range(0, 10):
    names.append("Triple-Fact %s" % i)

names += ["annotator-name"]

x = pd.DataFrame(data, columns=names)
x.to_csv(args.out)







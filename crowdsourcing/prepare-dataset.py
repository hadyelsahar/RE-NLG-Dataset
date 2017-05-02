##############################################
# Python script showing how many triples     #
# we have by annotator (with some details)   #
# like how many with dates, coreference, etc #
##############################################

import os
import json
import argparse
import pandas as pd
import csv
from unidecode import unidecode

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
__MAX_TRIPLES__ = 10
__MIN_TRIPLES__ = 2
__SAVE_N__ = 20
__MAX_WORDS__ = 80

path_to_properties = os.path.join(os.path.dirname(__file__), '../datasets/wikidata/wikidata-properties.csv')
properties = {}

with open(path_to_properties) as f:
    for l in csv.reader(f, delimiter='\t'):
        if l[1] == "http://www.w3.org/2000/01/rdf-schema#label":
            properties[l[0]] = l[2]

for file in os.listdir(args.input):
     with open(os.path.join(args.input, file)) as f:
         j = json.load(f)
         for d in j:

             # iterate over every document

             t = [x for x in d['triples'] if annotator_NosubSPO in x['annotator']]
             text = ""

             if len(t) > __MIN_TRIPLES__ and len(t) <= __MAX_TRIPLES__:

                 row = []
                 maxsent = 0

                 for c, x in enumerate(t):

                     if x['sentence_id'] > maxsent:

                         maxsent = x['sentence_id']


                     propname =  properties[x['predicate']['uri']] if x['predicate']['uri'] in properties else x['predicate']['surfaceform']

                     propname = "<b><font color=\"red\">" + propname + "</font></b>"
                     row.append("%s &nbsp;&nbsp;&nbsp; %s &nbsp;&nbsp;&nbsp; %s"% (d['title'], propname, x['object']['surfaceform']))
                 text = d['text'][0:d['sentences_boundaries'][maxsent][1]]
                 text = unidecode(text)

                 row = list(set(row))

                 if len(row) > __MAX_TRIPLES__:
                     row = row[0:__MAX_TRIPLES__]

                 elif len(row) < __MAX_TRIPLES__:
                     row += [None] * (__MAX_TRIPLES__ - len(row))

                 row = [text] + row
                 row += [x['annotator']]
                 data.append(row)
                 continue

             t = [x for x in d['triples'] if annotator_SPO in x['annotator']]
             if len(t) > __MIN_TRIPLES__ and len(t) <= __MAX_TRIPLES__:
                 row = []
                 maxsent = 0

                 for c, x in enumerate(t):

                     if x['sentence_id'] > maxsent:
                         maxsent = x['sentence_id']

                     propname = properties[x['predicate']['uri']] if x['predicate']['uri'] in properties else x['predicate']['surfaceform']
                     propname = "<b><font color=\"red\">" + propname + "</font></b>"

                     row.append(
                         "%s &nbsp;&nbsp;&nbsp; %s &nbsp;&nbsp;&nbsp; %s" % (d['title'], propname, x['object']['surfaceform']))

                 text = d['text'][0:d['sentences_boundaries'][maxsent][1]]
                 text = unidecode(text)

                 row = list(set(row))

                 if len(row) > __MAX_TRIPLES__:
                     row = row[0:__MAX_TRIPLES__]

                 elif len(row) < __MAX_TRIPLES__:
                     row += [None] * (__MAX_TRIPLES__ - len(row))

                 row = [text] + row
                 row += [x['annotator']]
                 data.append(row)
                 continue


             t = [x for x in d['triples'] if annotator_nosub in x['annotator']]
             if len(t) > __MIN_TRIPLES__ and len(t) <= __MAX_TRIPLES__:
                 row = []
                 maxsent = 0

                 for c, x in enumerate(t):

                     if x['sentence_id'] > maxsent:
                         maxsent = x['sentence_id']

                     if x['predicate']['uri'] in properties:

                        propname = properties[x['predicate']['uri']]

                     else:

                         continue

                     propname = "<b><font color=\"red\">" + propname + "</font></b>"
                     row.append(
                         "%s &nbsp;&nbsp;&nbsp; %s &nbsp;&nbsp;&nbsp; %s" % (d['title'], propname, x['object']['surfaceform']))
                 text = d['text'][0:d['sentences_boundaries'][maxsent][1]]
                 text = unidecode(text)

                 row = list(set(row))

                 if len(row) > __MAX_TRIPLES__:
                     row = row[0:__MAX_TRIPLES__]

                 elif len(row) < __MAX_TRIPLES__:
                     row += [None] * (__MAX_TRIPLES__ - len(row))

                 row = [text] + row
                 row += [x['annotator']]
                 data.append(row)
                 continue


             t = [x for x in d['triples'] if annotator_simple in x['annotator']]
             if len(t) > __MIN_TRIPLES__ and len(t) <= __MAX_TRIPLES__:
                 row = []
                 maxsent = 0

                 for c, x in enumerate(t):

                     if x['sentence_id'] > maxsent:
                         maxsent = x['sentence_id']


                     if x['predicate']['uri'] in properties:

                        propname = properties[x['predicate']['uri']]

                     else:

                         continue
                     propname = "<b><font color=\"red\">" + propname + "</font></b>"
                     row.append(
                         "%s &nbsp;&nbsp;&nbsp; %s &nbsp;&nbsp;&nbsp; %s" % (d['title'], propname, x['object']['surfaceform']))

                 text = d['text'][0:d['sentences_boundaries'][maxsent][1]]
                 text = unidecode(text)

                 row = list(set(row))

                 if len(row) > __MAX_TRIPLES__:
                     row = row[0:__MAX_TRIPLES__]

                 elif len(row) < __MAX_TRIPLES__:
                     row += [None] * (__MAX_TRIPLES__ - len(row))

                 row = [text] + row
                 row += [x['annotator']]
                 data.append(row)
                 continue


names = ["Original Sentence"]

for i in range(1, __MAX_TRIPLES__+1):
    names.append("Triple-Fact %s" % i)

names += ["annotator_name"]

x = pd.DataFrame(data, columns=names)


anns = set(x.annotator_name.values)
filtereddata = []

for ann in anns:
    tmp = [l for l in data if l[-1] == ann and len(l[0].split()) < __MAX_WORDS__]
    filtereddata += tmp[0:__SAVE_N__]

filteredx = pd.DataFrame(filtereddata, columns=names)
filteredx.to_csv(args.out, encoding="utf-8", index=False)









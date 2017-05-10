##################################################
# Script to read the output of the crowdsourcing #
# Experiment and analyse the results using       #
# for precision and recall and draw curves       #
##################################################

import os
import json
import argparse
import pandas as pd
import csv
from unidecode import unidecode
from collections import defaultdict


__VOTE__ = 0.5
# __max_annotators__ = 54
__max_facts__ = 10

parser = argparse.ArgumentParser(description='filter extracted attributes')
parser.add_argument('-i', '--input', help='input folder name', required=True)
parser.add_argument('-o', '--out', help='input file name', required=True)
args = parser.parse_args()

data = {} # {xxxxxx, original_sentence:,nfacts:,annotator:, nann:,annotations:[]}}
df = pd.read_csv(args.input)

def addline(row):
    global data

    if row['_unit_id'] not in data:

        nfacts = get_nfacts(row)
        nann = get_nann(row)
        annotations = get_annotations(row)

        if nfacts > 0 and nann > 0 and len(annotations) > 0:

            data[row['_unit_id']] = {
                "original_sentence": row['original_sentence'],
                "nfacts": nfacts,
                "nann": nann,
                "annotations": annotations,
                "ann_name": row['annotator_name']
            }
    else:

        k = data[row['_unit_id']]
        nfacts = k['nfacts']
        nann = k['nann']
        o = k['annotations']
        c = get_annotations(row)
        n = [o[i] + j for i, j in enumerate(c)]
        if len(c) > 0:
            data[row['_unit_id']]['annotations'] = n

def get_nfacts(row):
    for i in range(1,11):
        if row["%s__%s_triplefact_%s" % (i, i, i)] > 0:
            return i

    return 0

def get_nann(row):
    return df[df._unit_id == row._unit_id].shape[0]

def get_annotations(row):

    nfacts = get_nfacts(row)
    annotations = []
    for i in range(1, nfacts+1):
        tmp = 1 if row["%s__%s_triplefact_%s" % (i, nfacts, i)] else 0
        annotations.append(tmp)

    return annotations


for index, row in df.iterrows():
    addline(row)

x = pd.DataFrame(data.values())

def majority_vote(row):
    a = [0 if i/float(row["nann"]) <= __VOTE__ else 1 for i in row["annotations"]]
    return a

def inter_ann(row):
    a = [ 1- (abs((row["true"][c] * row["nann"]) - i) / float(row["nann"])) for c,i in enumerate(row["annotations"])]
    return a

x["true"] = x.apply(lambda a : majority_vote(a), axis=1)
x["interann"] = x.apply(lambda a : inter_ann(a), axis=1)
x.to_csv(args.out)


annotator_names = x.ann_name.unique()
nfacts = x.nfacts.unique()

results_annotators = defaultdict(list)
results_gold = {}
for n in nfacts:
    for ann in annotator_names:
        # shape = x[x.ann_name == ann][x.nfacts == n].shape[0]
        v = x[x.ann_name == ann][x.nfacts == n].true.values

        s1 = 0
        s2 = 0
        for i in v:
            for j in i:
                s1 += j
                s2 += 1

        r = s1/float(s2) if s2 > 0 else 0
        results_annotators[ann].append((n, r))

    v = x[x.ann_name == ann][x.nfacts == n].interann.values

    s1 = 0
    s2 = 0
    for i in v:
        for j in i:
            s1 += j
            s2 += 1

    r = s1 / float(s2) if s2 > 0 else 0
    results_annotators["golden"].append((n, r))





##############################################
#   Python script showing how many triples   #
#    a property has (with the annotators)    #
##############################################

import os
import json
import csv
import argparse
import pandas as pd
from collections import defaultdict


parser = argparse.ArgumentParser(description='filter extracted attributes')
parser.add_argument('-i', '--input', help='input file name', required=True)
parser.add_argument('-o', '--out', help='input file name', required=True)
args = parser.parse_args()

stats = defaultdict(int)

result = args.out
path_to_json = args.input

path_to_properties = os.path.join(os.path.dirname(__file__), '../datasets/wikidata/wikidata-properties.csv')
properties = defaultdict(list)

with open(path_to_properties) as f:
    for l in csv.reader(f, delimiter='\t'):
        properties[l[0]].append(l[2])


json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for c, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        print "Starting the file : " + str(os.path.join(path_to_json, js)) + " .. %s / %s" % (c+1, len(json_files))
        for d in json.load(json_file):
            for t in d['triples']:
		stats[(t['annotator'], t['predicate']['uri'])] += 1

with open(result, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for key, value in stats.items():
	label = '|'.join(properties[key[1]])
        spamwriter.writerow([key[0], key[1], label, value])

with open(result, 'r') as csvfile:
    reader = pd.read_csv(csvfile, ',', names=["annotator", "uri", "label", "count"])
    df = reader.sort_values("count", ascending=False)

with open(result, 'w') as writer:
    df.to_csv(writer, header=False, index=False)

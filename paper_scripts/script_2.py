##############################################
#   Python script showing how many triples   #
#    a property has (with the annotators)    #
##############################################

import os
import json
import csv
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser(description='filter extracted attributes')
parser.add_argument('-i', '--input', help='input file name', required=True)
parser.add_argument('-o', '--out', help='input file name', required=True)
args = parser.parse_args()

stats = defaultdict(int)

result = args.out
path_to_json = args.input

path_to_properties = os.path.join(os.path.dirname(__file__), '../datasets/wikidata/wikidata-properties.csv')
properties = defaultdict(str)

with open(path_to_properties) as f:
    for l in csv.reader(f, delimiter='\t'):
        properties[l[0]] = l[2]

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for c, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        print "Starting the file : " + str(os.path.join(path_to_json, js)) + " .. %s / %s" % (c+1, len(json_files))
        for d in json.load(json_file):
            for t in d['triples']:
                label = properties[t['predicate']['uri']]
		stats[(t['annotator'], t['predicate']['uri'], label)] += 1
                #stats["%s,%s,%s" % (t['annotator'], t['predicate']['uri'], label)] += 1

with open(result, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for key, value in stats.items():
        spamwriter.writerow([key[0], key[1], key[2], value])

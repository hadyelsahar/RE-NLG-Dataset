##############################################
#   Python script showing how many triples   #
#              an entity has                 #
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

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for c, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        print "Starting the file : " + str(os.path.join(path_to_json, js)) + " .. %s / %s" % (c+1, len(json_files))
        for d in json.load(json_file):
            for t in d['triples']:
		stats[(t['subject']['uri'], t['subject']['surfaceform'])] += 1
		stats[(t['object']['uri'], t['object']['surfaceform'])] += 1

with open(result, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for key, value in stats.items():
        spamwriter.writerow([key[0].encode('utf-8'), key[1].encode('utf-8'), value])

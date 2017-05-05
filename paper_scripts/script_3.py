##############################################
#   Python script showing how many triples   #
#              an entity has                 #
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

#stats = defaultdict(lambda: (list_dummy, 0))
stats = defaultdict(lambda: [0])

result = args.out
path_to_json = args.input

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for c, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        print "Starting the file : " + str(os.path.join(path_to_json, js)) + " .. %s / %s" % (c+1, len(json_files))
        for d in json.load(json_file):
            for t in d['triples']:
		if t['subject']['surfaceform'] not in stats[t['subject']['uri']]:
		    stats[t['subject']['uri']].append(t['subject']['surfaceform'])
		    stats[t['subject']['uri']][0] += 1
		else:
		    stats[t['subject']['uri']][0] += 1
		if t['object']['surfaceform'] not in stats[t['object']['uri']]:
                    stats[t['object']['uri']].append(t['object']['surfaceform'])
                    stats[t['object']['uri']][0] += 1
                else:
                    stats[t['object']['uri']][0] += 1


with open(result, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    for key, value in stats.items():
	label = '|'.join(stats[key][1:])
        spamwriter.writerow([key.encode('utf-8'), label.encode('utf-8'), stats[key][0]])

with open(result, 'r') as csvfile:
    reader = pd.read_csv(csvfile, ',', names=["uri", "label", "count"])
    df = reader.sort_values("count", ascending=False)

with open(result, 'w') as writer:
    df.to_csv(writer, header=False, index=False)

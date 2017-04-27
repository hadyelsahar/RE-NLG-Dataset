##############################################
#   Python script showing how many triples   #
#    a property has (with the annotators)    #
##############################################

import os
import json
import csv
from collections import defaultdict

stats = defaultdict(int)

result = os.path.join(os.path.dirname(__file__), '../results/result_script_2.json')
path_to_json = os.path.join(os.path.dirname(__file__), '../out')

path_to_properties = os.path.join(os.path.dirname(__file__), '../datasets/wikidata/wikidata-properties.csv')
properties = {}

with open(path_to_properties) as f:
    for l in csv.reader(f, delimiter='\t'):
        properties[l[0]] = l[2]

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for js in json_files:
    with open(os.path.join(path_to_json, js)) as json_file:
        for d in json.load(json_file):
            for t in d['triples']:
                label = properties[t['predicate']['uri']]
                stats["%s, %s, %s" % (t['annotator'], t['predicate']['uri'], label)] += 1
    json_file.close()

with open(result, 'w') as k:
    k.write(json.dumps(stats, indent=4))


k.close()
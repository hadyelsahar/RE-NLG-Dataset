##############################################
# Python script showing how many triples     #
# we have by annotator (with some details)   #
# like how many with dates, coreference, etc #
##############################################

import os
import json

annotator_date = "Date_Linker"
annotator_coref = "Simple_Coreference"
annotator_nosub = "NoSubject-Triple-aligner"
annotator_simple = "Simple-Aligner"
annotator_SPO = "SPOAligner"

stats = {
        "NoSubj_all" : 0,
        "NoSubj_dates" : 0,
        "Simple_all" : 0,
        "Simple_coref" : 0,
        "Simple_dates" : 0,
        "SPO_all" : 0,
        "SPO_coref" : 0,
        "SPO_dates" : 0
        }

result = os.path.join(os.path.dirname(__file__), '../results/result_script_1.json')
path_to_json = os.path.join(os.path.dirname(__file__), '../out')

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for js in json_files:
    with open(os.path.join(path_to_json, js)) as json_file:
        for d in json.load(json_file):
            for t in d['triples']:
                if t['annotator'] == annotator_nosub:
                    stats['NoSubj_all'] += 1
                    if t['subject']['annotator'] == annotator_date or t['object']['annotator'] == annotator_date:
                        stats['NoSubj_dates'] += 1
                elif t['annotator'] == annotator_simple:
                    stats['Simple_all'] += 1
                    if t['subject']['annotator'] == annotator_coref or t['object']['annotator'] == annotator_coref:
                        stats['Simple_coref'] += 1
                    if t['subject']['annotator'] == annotator_date or t['object']['annotator'] == annotator_date:
                        stats['Simple_dates'] += 1
                elif t['annotator'] == annotator_SPO:
                    stats['SPO_all'] += 1
                    if t['subject']['annotator'] == annotator_coref or t['object']['annotator'] == annotator_coref:
                        stats['SPO_coref'] += 1
                    if t['subject']['annotator'] == annotator_date or t['object']['annotator'] == annotator_date:
                        stats['SPO_dates'] += 1
    json_file.close()


with open(result, 'w') as k:
    k.write(json.dumps(stats, indent=4))


k.close()
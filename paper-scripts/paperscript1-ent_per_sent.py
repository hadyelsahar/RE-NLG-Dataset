
import argparse
import os
from os.path import join
import json
import pandas as pd

parser = argparse.ArgumentParser(description='python script to create chunks of nb wikipedia articles in separate files')
parser.add_argument('-i', '--input', help="path to wikipedia xml text corpus", required=True)
args = parser.parse_args()


counts = [(0, 0)]

for fname in os.listdir(args.input):
    with open(fname) as f:
        j = json.load(join(args.input, f))
        for d in j:
            for s in d['sentences_boundaries']:

                es = [e for e in d['entities'] if e['boundaries'][0] >= s[0] and e['boundaries'][1] <= s[1]]
                en = [e for e in es if e['annotator'] == "Wikidata_Spotlight_Entity_Linker"]

                counts.append((len(en), len(es)-len(en)))


x = pd.Series([i[0] for i in counts])
y = pd.Series([i[0] + i[1] for i in counts])

print (x.values_counts() / len(counts))[0:10]
print (y.values_counts() / len(counts))[0:10]

#################################################
# Python script showing the entities' name with #
# their URIs on Wikidata (to spot the ambiguous #
#                   entities)                   #
#################################################

import bz2
import os
import re
import json
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='filter extracted attributes')
parser.add_argument('-i', '--input', help='input file name', required=True)
parser.add_argument('-o', '--out', help='input file name', required=True)
args = parser.parse_args()

dump = args.input
result = os.path.join(args.out, 'result_script_0.json')

d = defaultdict(list)

with bz2.BZ2File(dump) as f:
    for l in f:
        pieces = [p for p in re.split("( |\\\".*?\\\"|'.*?')", l) if p.strip()]
        if pieces[1] == "<http://schema.org/name>":
            if pieces[3] == "@en":
                d[pieces[2]].append(pieces[0])

with open(result, 'w') as k:
    k.write(json.dumps(d, indent=4))
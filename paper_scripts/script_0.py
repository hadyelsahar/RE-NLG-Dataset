#################################################
# Python script showing the entities' name with #
# their URIs on Wikidata (to spot the ambiguous #
#                   entities)                   #
#################################################

import bz2
import os
import re
import json
from collections import defaultdict

dump = os.path.join(os.path.dirname(__file__), '../datasets/wikidata/wikidata-20170418-truthy-BETA.nt.bz2')
result = os.path.join(os.path.dirname(__file__), '../results/result_script_0.json')

d = defaultdict(list)

with bz2.BZ2File(dump) as f:
    for l in f:
        pieces = [p for p in re.split("( |\\\".*?\\\"|'.*?')", l) if p.strip()]
        if pieces[1] == "<http://schema.org/name>":
            if pieces[3] == "@en":
                d[pieces[2]].append(pieces[0])

f.close()
with open(result, 'w') as k:
    k.write(json.dumps(d, indent=4))
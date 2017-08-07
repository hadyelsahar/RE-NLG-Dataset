######################################################################################################
# script to convert a Wikidata dump to csv file and change it according to a given properties files #
######################################################################################################

import argparse
import bz2

parser = argparse.ArgumentParser(description='script to convert a Wikidata dump to csv file'
                                             'and change it according to a given properties files')
parser.add_argument('-i', '--input', help='Wikidata dump', required=True)
parser.add_argument('-p', '--properties', help='properties file', required=True)
parser.add_argument('-o', '--out', help='output file name', required=True)
args = parser.parse_args()

# reading properties
properties = []
with open(args.properties) as f:
    for l in f.readlines():
        properties.append(l.strip())

properties = set(properties)

out = open(args.out, "w")

with bz2.BZ2File(args.input) as f:
    for l in f:
        if "/prop/direct/P" not in l:
            continue
        tmp = l.split(' ')
        p = tmp[1][1:-1]
        if p in properties:
            s = tmp[0][1:-1]
            o = ' '.join(tmp[2:])[0:-2]
            if 'XMLSchema' not in o and 'Point' not in o:
                o = o[1:-2]
            out.write(s + '\t' + p + '\t' + o + '\n')

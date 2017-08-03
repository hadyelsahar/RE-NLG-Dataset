#################################################################################################################
# script to read datatypes from DBpedia instances types corpus and change it according to a given mappings files#
#################################################################################################################

import argparse

parser = argparse.ArgumentParser(description='script to read datatypes from DBpedia instances types corpus '
                                             'and change it according to a given mappings files')
parser.add_argument('-i', '--input', help='instances types file', required=True)
parser.add_argument('-m', '--mappings', help='mappings file', required=True)
parser.add_argument('-o', '--out', help='output file name', required=True)
args = parser.parse_args()

# reading mappings
mappings = {}
with open(args.mappings) as f:

    for l in f.readlines():
        tmp = l.split("\t")
        mappings[tmp[0].strip()] = tmp[1].strip()


out = open(args.out, "w")

with open(args.input) as f:

    for c, l in enumerate(f):
        uri1 = l.split("\t")[0]

        if uri1 in mappings:
            uri2 = mappings[uri1]
            out.write(l.replace(uri1, uri2))

        if (c+1) % 1000000 == 0:
            print "mapping types %s percent" % str(round(float(c*100)/len(mappings)))

out.close()






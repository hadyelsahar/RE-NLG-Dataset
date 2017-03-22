"""
Script to preprocess wikipedia-abstracts dump downloaded from DBpedia dataset
"""
__LOG_EVERY__=1000

import argparse

parser = argparse.ArgumentParser(description='Script to preprocess wikipedia-abstracts dump downloaded from DBpedia dataset')
parser.add_argument('-i', '--input', help="path to dbpedia abstracts dump", required=True)
# parser.add_argument('-o', '--output', help="output file path", required=True)
args = parser.parse_args()

c = 0
with open(args.input) as f:
    next(f)  # skip first line file header
    for l in f:

        # LOGGING
        c += 1
        if c % __LOG_EVERY__ == 0:
            print "%s file processed" % c

        try:

            tmp = l.split()
            print tmp[0][1:-1]
            title = tmp[0].strip()[0][1:-1]  # remove the <> in the beginning of the uri
            body = tmp[2].strip()[2:][1:-6]
            # print title

        except Exception as e:

            print e.message






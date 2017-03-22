"""
Script to preprocess wikipedia-abstracts dump downloaded from DBpedia dataset
"""
__LOG_EVERY__=1000

import argparse
import csv

parser = argparse.ArgumentParser(description='Script to preprocess wikipedia-abstracts dump downloaded from DBpedia dataset')
parser.add_argument('-i', '--input', help="path to dbpedia abstracts dump", required=True)
parser.add_argument('-o', '--output', help="output file path", required=True)
args = parser.parse_args()

c = 0
with open(args.input) as f:
    with open(args.output, 'w') as fout:
        writer = csv.writer(fout, delimiter='\t')
        next(f)  # skip first line file header

        for l in f:

            # LOGGING
            c += 1
            if c % __LOG_EVERY__ == 0:
                print "%s file processed" % c

            try:

                tmp = l.split()
                title = tmp[0][1:-1]  # remove the <> in the beginning of the uri
                body = " ".join(tmp[2:])[1:-6].replace("\\", "")  # nt format alraedy skipped -- unskip
                writer.writerow([title, body])

            except Exception as e:

                print e.message






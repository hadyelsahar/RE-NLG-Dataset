"""
Script to chunk wikipedia articles to fixed size atricles
"""

import argparse
from os import path

#######################
# LOADING INPUT FILES #
#######################

parser = argparse.ArgumentParser(description='python script to create chunks of nb wikipedia articles in separate files')
parser.add_argument('-i', '--input', help="path to wikipedia xml text corpus", required=True)
parser.add_argument('-o', '--output', help="output folder to save all generated json files", required=True)
parser.add_argument('-se', '--save_every', help="number of articles to save in each file", type=int, default=100000)
args = parser.parse_args()

doc_counter = 0
docstring = ""

with open(args.input) as f:
    for line in f:

        if line.startswith("<doc id="):
            doc_counter += 1

            if doc_counter % args.save_every == 0 and doc_counter != 0:
                fname = path.join(args.output, "doc_%08d-%08d.xml" % (doc_counter-args.save_every, doc_counter))

                with open(fname, 'w') as fout:
                    fout.write(docstring)
                print "Articles %08d - %08d ..done" % (doc_counter-args.save_every, doc_counter)
                docstring = ""

        docstring += line



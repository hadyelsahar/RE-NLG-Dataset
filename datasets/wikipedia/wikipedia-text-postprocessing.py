"""
A script to prepare RE-NLG Dataset out of a Wikipedia preprocessed text corpus


The Script outputs Number of files:

- documents.vocab:
        all vocabulary in the wikipedia articles

- documents.id:
        list of all document ids

-  NNNNN-of-NNNNN-doc.json:
        output file is json objects per line the keys of each json:

        "id":                       Wikipedia document id
        "title":                    title of the wikipedia document
        "wikidata_id":              Wikidata item id of the main page or None if doesn't exist
        "text":                     The whole text of the Wikipedia article
        "document_sequence_id":     list of IDS of words in the Wikipedia article
        "word_offsets":             list of offsets of each word in the Wikipedia Article
        "word_boundaries":          list of tuples (start, end) of each word in Wikipedia Article

contributors:
hadyelsahar@gmail.com
...

"""
import os
import csv
from collections import defaultdict
import argparse
import xml.etree.ElementTree as etree

import pandas as pd
from nltk import word_tokenize, sent_tokenize
import spotlight

####################
# GLOBAL VARIABLES #
####################
DOCS_PROCESSED_ID = []

BUFFER = []
TMP_BUFFER = []

LOG_EVERY_N = 1000
SAVE_EVERY_N = 10000
SAVE_DICT_EVERY_N = 100000

SPOTLIGHT_URL = 'http://localhost:2222/rest/annotate'
SPOTLIGHT_CONF = 0.4
SPOTLIGHT_SUPPORT = 1

MAX_WORD_ID = 0
SAVE_FIELDS_NAMES = ["id", "title", "wikidata_id", "text", "document_sequence_id", "word_offsets", "word_boundaries", "entities"]
###

#######################
# LOADING INPUT FILES #
#######################
parser = argparse.ArgumentParser(description='python script to create RE-NLG Data set of wikipedia dump')
parser.add_argument('input', help="path to wikipedia xml text corpus")
parser.add_argument('output', help="output folder to save all generated json files")
args = parser.parse_args()

wikiid_dict = pd.read_csv('./wiki_id-wikidataid.csv', names=["wikiid", "wikidataid"])
wikiid_dict = wikiid_dict.set_index('wikiid').to_dict()['wikidataid']
###

#########################
# INPUT FILE PROCESSING #
#########################

# creating a dict for indexing vocabulary
def adddocvocab():
    global MAX_WORD_ID
    MAX_WORD_ID += 1
    return [MAX_WORD_ID, 0]  # two int for each word [word_index_id, total_count]
documentvocab = defaultdict(lambda: adddocvocab)

print "Building index, removing categories and uninformative documents .."
for event, elem in etree.iterparse(args.input):

    # SAVING IF MATCH CONDITION
    if len(DOCS_PROCESSED_ID) % LOG_EVERY_N == 0:
        print "DOC: %s .." % COUNTER

    if len(BUFFER) % SAVE_EVERY_N == 0:

        fname = "%05d-of-%05d-doc.json" % (len(DOCS_PROCESSED_ID)-SAVE_EVERY_N, len(DOCS_PROCESSED_ID)-1)
        with open(os.join(args.output, fname), "a") as f:
            TMP_BUFFER = BUFFER
            BUFFER = []
            f.write("\n".join(TMP_BUFFER))

        with open("documents.id", "w") as f:
            f.write("\n".join([str(d) for d in DOCS_PROCESSED_ID]))

    if len(DOCS_PROCESSED_ID) % SAVE_DICT_EVERY_N == 0:
        with open('documents.vocab') as f:
            w = csv.writer(f)
            w.writerows(documentvocab.items())
    ###

    item = dict()

    # DOCUMENT IDS
    item["id"] = elem.attrib["id"]
    item["title"] = elem.attrib["title"]
    item["wikidata_id"] = wikiid_dict[item["id"]] if item["id"] in wikiid_dict else None

    # WORD INDEXING - BOUNDARIES INDEXING
    seq = word_tokenize(elem.text)
    sent = " ".join(seq)   # expanding all splits into spaces

    item["text"] = sent

    for w in word_tokenize(elem.text):
        documentvocab[w][1] += 1

    item["document_sequence_id"] = [documentvocab[w][0] for w in seq]

    word_offsets = []
    word_boundaries = []

    pr = 0
    for wc, w in enumerate(seq):
        s = pr
        e = s+len(w)
        word_offsets.append(s)
        word_boundaries.append((s, e))
        pr = e+1

    item["word_offsets"] = word_offsets
    item["word_boundaries"] = word_boundaries

    BUFFER.append({k: item[k] for k in SAVE_FIELDS_NAMES})



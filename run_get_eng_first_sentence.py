# a script to run TREx and get first english sentences for each entity in a given results file.
import argparse

from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.filter import *
from pipeline.writer import *


# Reading the DBpedia Abstracts Dataset
parser = argparse.ArgumentParser(description='a script to get first sentence from wikidata')
parser.add_argument('-wid', '--wikidataidsfile', help='Wikidata ids to limit', required=False)
args = parser.parse_args()

wids = set()

with open(args.wikidataidsfile) as f:
    for l in f:
        wids.add(l.strip())


reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', titles=wids)

# limiting sentences
sen_lim = SentenceLimiter()
writer = JsonWriter('./out_en_firstsent', "en")

for c, d in enumerate(reader.read_documents()):

    try:
        print "Processing Document Title: %s ..." % d.title

        print "sent limiter"
        d = sen_lim.run(d, 1)

        writer.run(d)
        print "Document %s .. Number of Annotated Entities %s \t Number of Annotated Triples %s \n -------" % (c, len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title




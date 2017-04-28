import multiprocessing
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import JsonWriter
from pipeline.coreference import *
from utils.triplereader import *
import argparse

__START_DOC__ = 0   #start reading from document number
__CORES__ = 3
# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', skip=__START_DOC__)

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
link = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=10, confidence=0.4)

coref = SimpleCoreference()
trip_read = TripleReader('./datasets/wikidata/wikidata-triples.csv')
Salign = SimpleAligner(trip_read)
prop = WikidataPropertyLinker('./datasets/wikidata/wikidata-properties.csv')
date = DateLinker()
SPOalign = SPOAligner(trip_read)
NSalign = NoSubjectAlign(trip_read)
writer = JsonWriter('./out', "re-nlg", startfile=__START_DOC__)


def reading_documents():
    # reading document and apply all non parallelizable process

    for d in reader.read_documents():
        d = date.run(d)                     # SU Time is non parallelizable
        yield d

def multhithreadprocess(d):

    try:

        d = link.run(d)
        d = coref.run(d)
        d = prop.run(d)
        d = NSalign.run(d)
        d = Salign.run(d)
        d = SPOalign.run(d)
        writer.run(d)
        print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title


if __name__ == '__main__':

    p = multiprocessing.Pool(__CORES__)
    p.map(multhithreadprocess, reading_documents())


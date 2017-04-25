import multiprocessing
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import JsonWriter
from pipeline.coreference import *
from utils.triplereader import *

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/sample-dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/sample-dbpedia-wikidata-sameas.csv')

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
link = WikidataSpotlightEntityLinker(db_wd_mapping='./datasets/wikidata/sample-dbpedia-wikidata-sameas.csv')
coref = SimpleCoreference()
trip_read = TripleReader('./datasets/wikidata/sample-wikidata-triples.csv')
Salign = SimpleAligner(trip_read)
prop = WikidataPropertyLinker('./datasets/wikidata/wikidata-properties.csv')
date = DateLinker()
SPOalign = SPOAligner(trip_read)
NSalign = NoSubjectAlign(trip_read)
writer = JsonWriter('./out', "baseline", 5)

def process_document(d):

    try:

        d = link.run(d)
        d = coref.run(d)
        d = prop.run(d)
        d = date.run(d)
        d = NSalign.run(d)
        d = Salign.run(d)
        d = SPOalign.run(d)
        print "Processing Document Title: %s " % (d.title)
        writer.run(d)
        print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title


if __name__ == '__main__':

    p = multiprocessing.Pool(5)
    p.map(process_document, reader.read_documents())


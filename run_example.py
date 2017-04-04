from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import JsonWriter
from pipeline.coreference import *

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/sample-dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/sample-dbpedia-wikidata-sameas.csv')

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
#link = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=10, confidence=0.4)
#link = DBSpotlightEntityLinker(spotlight_url='http://model.dbpedia-spotlight.org/en/annotate')
#link = WikidataSpotlightEntityLinker(db_wd_mapping='./datasets/wikidata/sample-dbpedia-wikidata-sameas.csv', spotlight_url='http://model.dbpedia-spotlight.org/en/annotate')
#coref = SimpleCoreference()
#align = SimpleAligner('./datasets/wikidata/sample-wikidata-triples.csv')
prop = WikidataPropertyLinker('./datasets/wikidata/wikidata-properties.csv')
#align = NoSubjectAlign('./datasets/wikidata/sample-wikidata-triples.csv')
#align = NoSubjectAlign('./datasets/wikidata/wikidata-triples.csv')
#writer = JsonWriter('./out')
for d in reader.read_documents():

    try:
        #d = link.run(d)
        #d = coref.run(d)
        #d = align.run(d)
        d = prop.run(d)
        if d is not None:
            print d.toJSON()
        else:
            print d
        # writer.run(d)
        #print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title

from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import JsonWriter


# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv')

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
link = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=10, confidence=0.4)
align = NoSubjectAlign('./datasets/wikidata/sample-wikidata-triples.csv')
writer = JsonWriter('./sample-docs', filesize=10)
for d in reader.read_documents():
    d = link.run(d)
    d = align.run(d)
    writer.run(d)
    print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

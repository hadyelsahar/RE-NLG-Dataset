import pandas as pd

from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import *
from pipeline.writer import JsonWriter
from pipeline.tuplealigner import TupleAligner

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReaderWithCoreNLP('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv')

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
# entitylinker = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', spotlight_url="http://model.dbpedia-spotlight.org/en/annotate", wikidata_types_dict="./datasets/wikidata/wikidata-types.csv", support=10, confidence=0.4)
entitylinker = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=10, confidence=0.4)

# reading list of patterns
patterns = pd.read_csv("./datasets/wikidata-properties/wikidata-properties-patterns-filtered.csv").pattern.values
propertylinker = POSPatternLinker(patterns, filter_annotator=[entitylinker.annotator_name], annotator_name="propertylinker")

ent_prop_aligner = TupleAligner(entitylinker.annotator_name, propertylinker.annotator_name, annotator_name="ent_prop_aligner", max_path_length=10)
ent_ent_aligner = TupleAligner(entitylinker.annotator_name, entitylinker.annotator_name, annotator_name="ent_ent_aligner", max_path_length=10)
writer = JsonWriter('./out', filesize=1000)

counter = 0 
for d in reader.read_documents():

    try:
        d = entitylinker.run(d)
        d = propertylinker.run(d)
        d = ent_ent_aligner.run(d)
        d = ent_prop_aligner.run(d)
        writer.run(d)
        print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Tuples %s" % (d.title, len(d.entities), len(d.tuples))
	counter += 1 
	if counter > 10000:
		break 

    except Exception as e:

        print "error Processing document %s" % d.title
        print e.message



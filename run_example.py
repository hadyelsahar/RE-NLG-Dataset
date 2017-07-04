from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import JsonWriter
from pipeline.coreference import *
from utils.triplereader import *
from utils.triplereaderitems import *
from utils.labelreader import *

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/sample-dbpedia-abstracts-eo.csv', db_wd_mapping='./datasets/wikidata/sample-dbpedia-wikidata-sameas.csv')

# LabelReader for esperanto
label_read = LabelReader('./datasets/wikidata/sample-wikidata-labels.csv', 'eo')
trip_read_items = TripleReaderItems('./datasets/wikidata/sample-wikidata-triples.csv')
keyword_ent_linker = KeywordMatchingEntityLinker(trip_read_items, label_read)
# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
# link = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=10, confidence=0.4)
# link = DBSpotlightEntityLinker(spotlight_url='http://model.dbpedia-spotlight.org/en/annotate')
#link = WikidataSpotlightEntityLinker(db_wd_mapping='./datasets/wikidata/sample-dbpedia-wikidata-sameas.csv', spotlight_url='http://model.dbpedia-spotlight.org/en/annotate')
#coref = SimpleCoreference()
trip_read = TripleReader('./datasets/wikidata/sample-wikidata-triples.csv')
Salign = SimpleAligner(trip_read)
prop = WikidataPropertyLinker('./datasets/wikidata/wikidata-properties.csv')
#date = DateLinker()
#SPOalign = SPOAligner(trip_read)
NSalign = NoSubjectAlign(trip_read)
writer = JsonWriter('./out-test', "", 1)

for d in reader.read_documents():
	#print d.title

	#print label_read.get(d.docid)
#    try:
	d = keyword_ent_linker.run(d)
		#d = link.run(d)
	d = NSalign.run(d)
		#d = coref.run(d)
		#d = date.run(d)
	d = Salign.run(d)
		#d = prop.run(d)
		#d = SPOalign.run(d)
	writer.run(d)
	print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

 #   except Exception as e:

  #      print "error Processing document %s" % d.title

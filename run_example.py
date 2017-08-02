from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import *
from pipeline.coreference import *
from utils.triplereader import *
from utils.triplereaderitems import *
from utils.triplereadertriples import *
from utils.labelreader import *
from pipeline.filter import *

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/sample-dbpedia-abstracts-ar.csv')

trip_read = TripleReader('./datasets/wikidata/sample-wikidata-triples.csv')
label_read = LabelReader('./datasets/wikidata/sample-wikidata-labels.csv', 'ar')
trip_read_items = TripleReaderItems('./datasets/wikidata/sample-wikidata-triples.csv')
trip_read_trip = TripleReaderTriples('./datasets/wikidata/sample-wikidata-triples.csv')

keyword_ent_linker = KeywordMatchingEntityLinker(trip_read_items, label_read)
salign = SimpleAligner(trip_read)

#prop = WikidataPropertyLinker('./datasets/wikidata/wikidata-properties.csv')
date = DateLinker()
#SPOalign = SPOAligner(trip_read)
nsalign = NoSubjectAlign(trip_read)
noalign = NoAligner(trip_read_trip)

disam_lim = RemoveDisambiguationPagesLimiter(trip_read_trip)
fist_sen_lim = FistSentenceLimiter()
main_ent_lim = MainEntityLimiter()

writer = JsonWriter('./out-test', "", 1)

writer_triples = CustomeWriterTriples('./out-test', "", 1)
writer_entities = CustomeWriterEntities('./out-test', "", 1)

for d in reader.read_documents():
	#print d.title

	#print label_read.get(d.docid)
#    try:
	if not disam_lim.run(d):
		print d.docid
		continue

	d = keyword_ent_linker.run(d)
	d = date.run(d)
		#d = link.run(d)
	d = nsalign.run(d)
		#d = coref.run(d)
		#d = date.run(d)
	d = salign.run(d)
		#d = prop.run(d)
		#d = SPOalign.run(d)
	d = fist_sen_lim.run(d)

	if not main_ent_lim.run(d):
		continue

	d = noalign.run(d)

	writer_triples.run(d)
	writer_entities.run(d)
	writer.run(d)
	print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

 #   except Exception as e:

  #      print "error Processing document %s" % d.title

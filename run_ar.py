from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *
from pipeline.typetaggers import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.writer import *
# from pipeline.coreference import *
from utils.triplereader import *
from utils.triplereaderitems import *
from utils.triplereadertriples import *
from utils.labelreader import *
from pipeline.filter import *

start_doc = 0   #start reading from document number #

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts-ar.csv', skip=start_doc)

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
# link = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=10, confidence=0.4)

#coref = SimpleCoreference()
trip_read = TripleReader('./datasets/wikidata/wikidata-triples.csv')
label_read = LabelReader('./datasets/wikidata/wikidata-labels.csv', 'ar')
trip_read_items = TripleReaderItems('./datasets/wikidata/wikidata-triples.csv')
trip_read_trip = TripleReaderTriples('./datasets/wikidata/wikidata-triples.csv')

keyword_ent_linker = KeywordMatchingEntityLinker(trip_read_items, label_read)
Salign = SimpleAligner(trip_read)
#prop = WikidataPropertyLinker('./datasets/wikidata/wikidata-properties.csv')
date = DateLinker()
#SPOalign = SPOAligner(trip_read)
NSalign = NoSubjectAlign(trip_read)
Noalign = NoAligner(trip_read_trip)

filter_entities = ['http://www.wikidata.org/entity/Q4167410', 'http://www.wikidata.org/entity/Q13406463']
ent_filt = EntityTypeFilter(trip_read_trip, filter_entities)
sen_lim = SentenceLimiter()
main_ent_lim = MainEntityLimiter()

prop_tag = PropertyTypeTagger()

writer_triples = CustomeWriterTriples('./out_ar', "re-nlg", startfile=start_doc)
writer_entities = CustomeWriterEntities('./out_ar', "re-nlg", startfile=start_doc)
writer = JsonWriter('./out_eo', "re-nlg", startfile=start_doc)

for d in reader.read_documents():

    try:
        print "Processing Document Title: %s ..." % d.title

        if not ent_filt.run(d):
            continue

        d = keyword_ent_linker.run(d)

        d = date.run(d)
        d = NSalign.run(d)

        #d = coref.run(d)
        d = Salign.run(d)

        #d = prop.run(d)
        #d = SPOalign.run(d)
        d = sen_lim.run(d, 0)

        if not main_ent_lim.run(d):
            continue

        d = Noalign.run(d)

        d = prop_tag.run(d)

        writer_triples.run(d)
        writer_entities.run(d)
        writer.run(d)
        print "Number of Annotated Entities %s \t Number of Annotated Triples %s \n -------" % (len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title

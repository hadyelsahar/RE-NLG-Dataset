from utils.triplereadertriples import *
from pipeline.datareader import DBpediaAbstractsDataReader
from pipeline.triplealigner import *
from pipeline.entitylinker import *
from pipeline.filter import *
from pipeline.writer import *
from pipeline.coreference import *
from pipeline.placeholdertagger import *

start_doc = 0   #start reading from document number #

# Reading the DBpedia Abstracts Dataset
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', skip=start_doc)

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
link = WikidataSpotlightEntityLinkerWithCustomSupportAndFilter('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv')
coref = SimpleCoreference()

trip_read_trip = TripleReaderTriples('./datasets/wikidata/wikidata-triples.csv')

# filters and limiters
filter_entities = ['http://www.wikidata.org/entity/Q4167410', 'http://www.wikidata.org/entity/Q13406463']
entity_filter = EntityTypeFilter(trip_read_trip, filter_entities)

# limiting sentences
sen_lim = SentenceLimiter()

# checking if main entity of the document is found by an entity linker
main_ent_lim = MainEntityLimiter()

# placholder creation
placeholder_tagger = TypePlaceholderTagger('./datasets/datatypes/wikidata_datatypes.csv')
prop_tag = PropertyPlaceholderTagger()

# adding triples from a knowledge base
noalign = NoAligner(trip_read_trip)

writer_triples = CustomeWriterTriples('./out-jws', "jws_trex", 10000)
writer_entities = CustomeWriterEntities('./out-jws', "jws_trex", 10000)
writer = JsonWriter('./out-jws', "jws_trex")


for d in reader.read_documents():

    try:
        print "Processing Document Title: %s ..." % d.title


        if not entity_filter.run(d):
            continue

        d = sen_lim.run(d, 0)

        d = link.run(d)

        if not main_ent_lim.run(d):
            continue

        d = coref.run(d)

        d = coref.run(d)

        d = noalign.run(d)

        d = prop_tag.run(d)

        writer_triples.run(d)
        writer_entities.run(d)
        writer.run(d)
        print "Number of Annotated Entities %s \t Number of Annotated Triples %s \n -------" % (len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title




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
reader = DBpediaAbstractsDataReader('./datasets/wikipedia-abstracts/csv/dbpedia-abstracts.csv', db_wd_mapping='./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', skip=start_doc, titles='./datasets/bibliography_titles.tsv')

# Loading the WikidataSpotlightEntityLinker ... DBpedia Spotlight with mapping DBpedia URIs to Wikidata
link = WikidataSpotlightEntityLinkerWithCustomSupportAndFilter('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', spotlight_url="http://127.0.0.1:2222/rest/annotate")
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


for c, d in enumerate(reader.read_documents()):

    try:
        print "Processing Document Title: %s ..." % d.title


        print "entity filter"
        if not entity_filter.run(d):
            continue

        print "sent limiter"
        d = sen_lim.run(d, 1)

        print "linking"
        d = link.run(d)

        if not main_ent_lim.run(d):
            continue

        # d = coref.run(d)

        print "triple alignment"
        d = noalign.run(d)

        print "adding placeholders"
        d = placeholder_tagger.run(d)
        d = prop_tag.run(d)

        print "writing to buffer"
        writer_triples.run(d)
        writer_entities.run(d)
        writer.run(d)
        print "Document %s .. Number of Annotated Entities %s \t Number of Annotated Triples %s \n -------" % (c, len(d.entities), len(d.triples))

    except Exception as e:

        print "error Processing document %s" % d.title




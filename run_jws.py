
from utils.triplereadertriples import *

from pipeline.datareader import TRExDataReader

from pipeline.placeholdertagger import TypePlaceholderTagger
from pipeline.triplealigner import *

from pipeline.filter import *
from pipeline.writer import *
from pipeline.placeholdertagger import *

# Read titles of files from the bibliography domain


# Reading the T-REx premade dataset folder
reader = TRExDataReader('./out/')
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

writer = JsonWriter('./out-jws', "", 1000)
writer_triples = CustomeWriterTriples('./out-jws', "jws_trex", 10000)
writer_entities = CustomeWriterEntities('./out-jws', "jws_trex", 10000)

for d in reader.read_documents():

    # try:
        if not entity_filter.run(d):
            continue

        d = sen_lim.run(d, 1)

        if not main_ent_lim.run(d):
            continue

        d = placeholder_tagger.run(d)

        d = noalign.run(d)
        d = prop_tag.run(d)

        writer_triples.run(d)
        writer_entities.run(d)
        writer.run(d)
        print "Document Title: %s \t Number of Annotated Entities %s \t Number of Annotated Triples %s" % (d.title, len(d.entities), len(d.triples))

    # except Exception as e:
    #     print "error Processing document %s" % d.title

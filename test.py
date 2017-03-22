from pipeline.pipeline import *
from pipeline.entitylinker import *
from pipeline.triplealigner import *

x = "Dutch language is the official language of the Netherlands, "
d = Document('101010', "Netherlands", "http://www.wikidata.org/entity/Q55", x)
link = WikidataSpotlightEntityLinker('./datasets/wikidata/dbpedia-wikidata-sameas-dict.csv', support=1, confidence=0.2)
align = NoSubjectAlign('./datasets/wikidata/sample-wikidata-triples.csv')

d = link.run(d)
d = align.run(d)
print d.toJSON()


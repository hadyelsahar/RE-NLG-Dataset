from collections import defaultdict

# Create a defaultdict {entity:[entity, entity]}
class TripleReaderTriples:

    def __init__(self, triples_file):

        self.baseuri = "http://www.wikidata.org/entity/"
        self.baseuripred = "http://www.wikidata.org/prop/direct/"

        self.d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")

                # check whether object is also an entity
                if self.baseuri in tmp[2]:
                    subj_id = tmp[0].strip().replace(self.baseuri, "")
                    obj_id = tmp[2].strip().replace(self.baseuri, "")
                    subj = tmp[0].strip()
                    pred = tmp[1].strip()
                    obj = tmp[2].strip()
                    # create triples for each line
                    triple = [subj, pred, obj]

                    # We want to have the entity whether it's object or subject
                    self.d[subj_id].append(triple)
                    self.d[obj_id].append(triple)

    def get(self, uri):
        # return triples for given entity id
        return self.d[uri.strip().replace(self.baseuri, "")]
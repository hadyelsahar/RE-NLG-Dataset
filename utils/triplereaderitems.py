from collections import defaultdict

# Create a defaultdict {entity:[entity, entity]}
class TripleReaderItems:

    def __init__(self, triples_file):

        self.baseuri = "http://www.wikidata.org/entity/"

        self.d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")
                if len(tmp) < 3:
                    continue
                # check whether object is also an entity
                if self.baseuri in tmp[2]:
                    subj = tmp[0].strip().replace(self.baseuri, "")
                    obj = tmp[2].strip().replace(self.baseuri, "")
                    # We want to have the entity whether it's object or subject
                    self.d[subj].append(obj)
                    self.d[obj].append(subj)

    def get(self, uri):
        p = self.d[uri.strip().replace(self.baseuri, "")]
        # add the key as a value to keep it as possible entity ID
        p.append(uri.strip().replace(self.baseuri, ""))
        return set(["%s%s" % (self.baseuri, i) for i in p])
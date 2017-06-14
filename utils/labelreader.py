from collections import defaultdict

# create a defaultdict {entity:[label, alias, alias], entity:[label, alias]}
# from a csv file of labels formatted as "Q12345 \t 'Count von Count' \t en"
# TODO: language fallback
class LabelReader:

    def __init__(self, labels_file, lang=None):

        self.baseuri = "http://www.wikidata.org/entity/"

        self.d = defaultdict(list)
        self.fallback = defaultdict(list)
        with open(labels_file) as f:
            for l in f:
                tmp = l.split("\t")
                entity_id = tmp[0].strip().replace(self.baseuri, "")

                #if no language is set
                if lang == None:
                    self.d[entity_id].append(tmp[1].strip())
                    continue

                #if language is set
                if tmp[2].strip() == lang:
                    self.d[entity_id].append(tmp[1].strip())
                #start building something for language fallback
                elif not self.d[entity_id]:
                    self.fallback[entity_id].append({tmp[2].strip(): tmp[1].strip()})
                    self.d[entity_id] = []

    def get(self, uri):
        p = self.d[uri.strip().replace(self.baseuri, "")]
        return [i for i in p]
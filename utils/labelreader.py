from collections import defaultdict

# return a defaultdict {entity:{lang:{"label", "alias"}, lang:{"label", "alias", "alias"} }} 
# from a csv file of labels formatted as "Q12345 \t 'Count von Count' \t en"
class LabelReader:

    def __init__(self, labels_file, lang):

        self.baseuri = "http://www.wikidata.org/entity/"

        self.d = defaultdict(list)
        self.fallback = defaultdict(list)
        with open(labels_file) as f:
            for l in f:
                tmp = l.split("\t")
                # TODO: language fallback
                if tmp[2].strip() == lang:
                    self.d[tmp[0].strip().replace(self.baseuri, "")].append(tmp[1].strip())


    def get(self, uri):
        p = self.d[uri.strip().replace(self.baseuri, "")]
        return [i for i in p]
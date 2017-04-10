from collections import defaultdict


class TripleReader:

    def __init__(self, triples_file):
        self.d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")
                self.d["%s\t%s" % (tmp[0].strip(), tmp[2].strip())].append(tmp[1])

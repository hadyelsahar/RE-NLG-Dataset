from collections import defaultdict

class TripleReader:

    def __init__(self, triples_file):

        self.baseuripred = 'http://www.wikidata.org/prop/direct/'
        self.baseuriobj = 'http://www.wikidata.org/entity/'

        self.d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")
                self.d["%s%s" %
                       (tmp[0].strip().replace(self.baseuriobj, ''),
                        tmp[2].strip().replace(self.baseuriobj, ''))].append(tmp[1].replace(self.baseuripred, ''))

    def get(self, suri, objuri):
        return "%s%s" % (self.baseuripred,
                          self.d["%s%s" %
                                (suri.strip().replace(self.baseuriobj, ''), objuri.strip().replace(self.baseuriobj, ''))
                                ]
                         )
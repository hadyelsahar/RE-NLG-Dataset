__author__ = 'hadyelsahar'

import json

import numpy as np
import networkx as nx
import requests


class CoreNlPClient:

    def __init__(self, serverurl="http://127.0.0.1:9000/", annotators=("tokenize", "ssplit", "pos", "lemma", "ner", "parse", "dcoref")):

        self.properties = {}
        self.properties["annotators"] = ",".join(annotators)
        self.properties["tokenize.whitespace"] = False
        self.properties["outputFormat"] = "json"
        self.serverurl = serverurl

    def annotate(self, s):

        properties = json.dumps(self.properties)
        r = requests.post("%s?properties=%s" %(self.serverurl, properties), data=s)

        if r.status_code == 200:
            x = json.loads(unicode(r.text), strict=False)

            return Parse(x)

        else:
            raise RuntimeError("%s \t %s"%(r.status_code, r.reason))


class Parse:
    """
    a class to hold the output of the corenlp parsed result
    """
    def __init__(self, parsed):
        """
        :param parsed: the output of invoking the stanford parser service
        :return
            tokens: list of tokens in text
            positions: tuples contains start and end offsets of every token
            postags: list of pos tags for every token
            ner: list of ner tags for every token
            parsed_tokens:
                    for every token list all incoming or out-coming relations
                    redundant but easy to call afterwards when writing rule based
                    {"in":[], "out":[]}] ... etc
        """

        self.tokens = [i['originalText'] for i in parsed["sentences"][0]["tokens"]]
        self.positions = [(i['characterOffsetBegin'], i['characterOffsetEnd']) for i in parsed["sentences"][0]["tokens"]]
        self.postags = [i['pos'] for i in parsed["sentences"][0]["tokens"]]
        self.ner = [i['ner'] for i in parsed["sentences"][0]["tokens"]]
        self.parsed_tokens = parsed["sentences"][0]["tokens"]

        # removing the root note and starting counting from 0
        self.dep = [{"in": [], "out":[]} for i in self.tokens]

        for d in parsed["sentences"][0]["collapsed-ccprocessed-dependencies"]:

            if d['dep'] == "ROOT":
                self.dep[d['dependent']-1]["in"].append(("ROOT", None))

            else:
                self.dep[d['dependent']-1]["in"].append((d['dep'], d['governor']-1))
                self.dep[d['governor']-1]["out"].append((d['dep'], d['dependent']-1))

        self.corefs = parsed["corefs"]
        self.all = parsed

        # making graphs out of parses to make shortest path function
        self.depgraph = nx.MultiDiGraph()
        for tokid, dep in enumerate(self.dep):
            for iin in dep['in']:
                self.depgraph.add_edge(iin[1], tokid, label=iin[0])

    def getshortestpath(self, source, target):

        try:
            path = nx.shortest_path(self.depgraph, source=source, target=target)

            s = ""

            for c, i in enumerate(path[:-1]):

                if c != 0:
                    s += " -> "
                    s += self.tokens[i]
                s += " -> "
                s += self.depgraph.get_edge_data(i, path[c+1])[0]['label']

            s += " -> "
            # s += self.tokens[path[-1]]

            return s

        except:
            return None


    def getchunks_using_patterns(self, patterns, sequence, removesubsets=True):
        """
        get chunks is a function that returns array of arrays containing chunks repreresenting specific patterns in the
        parsed sentence  ex : [[1, 2], [4, 5], [11, 12]]
        :param patterns: array of arrays representing patterns [['NN'], ['NN','NN','NP'],['VP', 'NP']]
        :param sequence: the sequence of tags to apply patterns on [self.ner, self.postags, self.tokens]
        :param inclusive: get all patterns matches regarding if they intersect with or not.
        :return:arrays containing chunks repreresenting specific patterns in the
        parsed sentence  ex : [[1, 2], [4, 5], [11, 12]]
        """

        def index(subseq, seq):
            """
            Return an index of `subseq`uence in the `seq`uence.
            Or `-1` if `subseq` is not a subsequence of the `seq`.
            The time complexity of the algorithm is O(n*m), where
                n, m = len(seq), len(subseq)
            index([1,2], range(5))
            [1]
            index(range(1, 6), range(5))
            -1
            index(range(5), range(5))
            [0]
            index([1,2], [0, 1, 0, 1, 2])
            [3]
            index([1,2], [0, 1,2 , 0, 1, 2])
            [1,4]
            """
            starts = []
            # while subseq[0] in seq:
            #     index = seq.index(subseq[0])
            #     if subseq == seq[index:index + len(subseq)]:
            #         starts.append(index)
            #     else:
            #         seq = seq[index + 1:]
            #
            # if len(starts) > 0:
            #     return starts
            # else:
            #     return -1

        allchunks = []

        # extraction of chunks that exists in patterns
        for pattern in patterns:
            starts = np.where(np.array(sequence) == pattern[0])[0]

            l = len(pattern)
            for start in starts:
                if sequence[start:start+l] == pattern:
                    allchunks.append(set(range(start, start+l)))

        # filteration of patterns and remove chunks who are subsets of other chunks keeping only the larger ones
        if not removesubsets:
            return allchunks

        else:
            chunkstoreturn = []
            for chunk1 in allchunks:

                is_subset_of_other = False

                for chunk2 in allchunks:
                    # no need to remove chunk1 because we are going to check for only subsets not equality
                    if chunk1 < chunk2:
                        is_subset_of_other = True
                        break

                if not is_subset_of_other:
                    chunkstoreturn.append(sorted(list(chunk1)))

            return chunkstoreturn
__author__ = 'hadyelsahar'

import json
import numpy as np
import requests
from pipeline.pipeline import *


class CoreNlPClient:

    def __init__(self, serverurl="http://127.0.0.1:9000/", annotators=("tokenize", "ssplit", "pos", "lemma", "ner", "parse", "dcoref")):

        self.properties = {}
        self.properties["annotators"] = ",".join(annotators)
        self.properties["tokenize.whitespace"] = False
        self.properties["outputFormat"] = "json"
        self.serverurl = serverurl

    def annotate(self, s):

        properties = json.dumps(self.properties)
        r = requests.post("%s?properties=%s" % (self.serverurl, properties), data=s)

        if r.status_code == 200:
            x = json.loads(unicode(r.text), strict=False)

            return Parse(x, annotators=self.properties["annotators"])

        else:
            raise RuntimeError("%s \t %s" % (r.status_code, r.reason))


class Parse:
    """
    a class to hold the output of the corenlp parsed result
    """
    def __init__(self, parsed, annotators):
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
        self.tokens = []
        self.sentences_boudaries = []
        self.words_boudaries = []
        self.postags = None
        self.ner = None
        self.dep = None

        sentence_start_token = 0
        for s in parsed["sentences"]:
            # get sentence boundaries
            start = s['tokens'][0]["characterOffsetBegin"]
            end = s['tokens'][-1]["characterOffsetEnd"]

            self.sentences_boudaries.append((start, end))

            self.tokens += [i["originalText"] for i in s["tokens"]]
            self.words_boudaries += [(i['characterOffsetBegin'], i['characterOffsetEnd']) for i in s["tokens"]]

            if "pos" in annotators:
                if self.postags is None:
                    self.postags = []
                self.postags += [i['pos'] for i in s["tokens"]]

            if "ner" in annotators:
                if self.ner is None:
                    self.ner = []
                self.ner += [i['ner'] for i in s["tokens"]]

            if "parse" in annotators:
                if self.dep is None:
                    self.dep = []
                # removing the root note and starting counting from token base
                for d in s["collapsed-ccprocessed-dependencies"]:

                    d['dependent'] = d['dependent'] - 1 + sentence_start_token

                    if d['governor'] == 0:
                        d['governor'] = -1   # -1 is the governor of all root words in all the sentences

                    else:
                        d['governor'] = d['governor'] - 1 + sentence_start_token

                    self.dep.append(d)

            sentence_start_token += len(s['tokens'])

        # # making graphs out of parses to make shortest path function
        # self.depgraph = nx.MultiDiGraph()
        # for tokid, dep in enumerate(self.dep):
        #     for iin in dep['in']:
        #         self.depgraph.add_edge(iin[1], tokid, label=iin[0])

    # def getshortestpath(self, source, target):
    #
    #     try:
    #         path = nx.shortest_path(self.depgraph, source=source, target=target)
    #
    #         s = ""
    #
    #         for c, i in enumerate(path[:-1]):
    #
    #             if c != 0:
    #                 s += " -> "
    #                 s += self.tokens[i]
    #             s += " -> "
    #             s += self.depgraph.get_edge_data(i, path[c+1])[0]['label']
    #
    #         s += " -> "
    #         # s += self.tokens[path[-1]]
    #
    #         return s
    #
    #     except:
    #         return None


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
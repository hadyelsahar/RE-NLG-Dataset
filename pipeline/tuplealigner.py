from pipeline import *
from entitylinker import *
from collections import defaultdict
import networkx as nx


class TupleAligner(BasePipeline):

    def __init__(self, entity_aliners, property_aligners, annotator_name, max_path_length=5):

        self.entity_aligners = entity_aliners
        self.property_aligners = property_aligners
        self.annotator_name = annotator_name
        self.max_path_length = max_path_length

    def run(self, document):
        """
        :param: input document to align it's sentences with triples
        :return:
        """
        document.tuples = []

        ### Building a graph of Dependency Edges ###
        # make a graph of dependency
        graph = nx.Graph()

        for i, w in enumerate(document.words_boundaries):
            graph.add_node(i, label=document.text[w[0]:w[1]])

        for i in document.dependencies:

            # tmp = document.words_boundaries[i.govid]
            # gov_label = document.text[tmp[0]:tmp[1]]
            # tmp = document.words_boundaries[i.depid]
            # dep_label = document.text[tmp[0]:tmp[1]]
            edge_label = "> %s >" % i.dep
            graph.add_edge(i.govid, i.depid, label=edge_label)

        for sid, (start, end) in enumerate(document.sentences_boundaries):

            entities = [i for i in document.entities if i.annotator in self.entity_aligners and i.boundaries[0] >= start and i.boundaries[1] <= end]
            properties = [i for i in document.entities if i.annotator in self.property_aligners and i.boundaries[0] >= start and i.boundaries[1] <= end]

            for e in entities:
                for p in properties:

                    e_word_ids = [i for i, b in enumerate(document.words_boundaries) if b[0] >= e.boundaries[0] and b[1] <= e.boundaries[1]]
                    p_word_ids = [i for i, b in enumerate(document.words_boundaries) if b[0] >= p.boundaries[0] and b[1] <= p.boundaries[1]]

                    connected = False
                    path = []
                    for i in e_word_ids:
                        for j in p_word_ids:

                            try:
                                path = nx.shortest_path(graph, source=i, target=j)
                            except Exception:
                                pass

                            # has to be larger than one
                            # eliminating comparison by a node and itself which will return a path of size 1
                            if  1< len(path) < self.max_path_length:
                                connected = True
                                break

                    if connected:
                        lexicalized_dependency_path = ""

                        for c, i in enumerate(path[:-1]):
                            lexicalized_dependency_path += document.text[
                                                           document.words_boundaries[i][0]:document.words_boundaries[i][
                                                               1]]
                            lexicalized_dependency_path += " "
                            lexicalized_dependency_path += graph.get_edge_data(i, path[c + 1])['label']
                            lexicalized_dependency_path += " "

                        lexicalized_dependency_path += document.text[document.words_boundaries[path[-1]][0]:
                        document.words_boundaries[path[-1]][1]]

                        document.tuples.append(Tuple(
                            subject=e,
                            predicate=p,
                            direction=1,
                            sentence_id=sid,
                            dependency_path=lexicalized_dependency_path,
                            annotator=self.annotator_name
                        ))

        return document

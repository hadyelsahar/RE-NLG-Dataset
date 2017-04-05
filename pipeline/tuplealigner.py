
from pipeline import *
from entitylinker import *
from collections import defaultdict
import networkx as nx
class TupleAligner(BasePipeline):

    annotator_name = "tuple-aligner"


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

            tmp = document.words_boundaries[i.govid]
            gov_label = document.text[tmp[0]:tmp[1]]
            tmp = document.words_boundaries[i.depid]
            dep_label = document.text[tmp[0]:tmp[1]]
            edge_label = "> %s > " %(gov_label, i.dep, dep_label)
            graph.add_edge((i.govid, i.depid), label=edge_label)


        for sid, (start, end) in enumerate(document.sentences_boundaries):

            # Getting sentence subject
            # Every sentence has main entity as subject
            entities = [i for i in document.entities if i.annotator == WikidataSpotlightEntityLinker.annotator_name and i.boundaries[0] >= start and i.boundaries[1] <= end]
            properties = [i for i in document.entities if i.annotator == POSPatternLinker.annotator_name and i.boundaries[0] >= start and i.boundaries[1] <= end]

            for e in entities:
                for p in properties:

                    e_word_ids = [i for i, b in document.words_boundaries if b[0] >= e.boundaries[0] and b[1] <= e.boundaries[1]]
                    p_word_ids = [i for i, b in document.words_boundaries if b[0] >= p.boundaries[0] and b[1] <= p.boundaries[1]]

                    conntected = False
                    path = []
                    for i in e_word_ids:
                        for j in p_word_ids:

                            try:
                                path = nx.shortest_path(graph, source=i, target=j)
                            except Exception as e:
                                pass

                            if len(path) > 0:
                                conntected = True
                                break

                    if conntected:
                        document.tuples.append(Tuple(
                            subject=e,
                            predicate=p,
                            direction=1,
                            sentence_id=sid,
                            dependency_path=path
                        ))

        return document

from pipeline import *
from collections import defaultdict
import itertools


class NoSubjectAlign(BasePipeline):
    """
    Following the assumption in NoSUB  [1] and [2] that sentences in one paragraph all share the same subject.
    [1] Augenstein, Isabelle, Diana Maynard, and Fabio Ciravegna. "Distantly supervised web relation extraction for knowledge base population." Semantic Web 7.4 (2016): 335-349.
    [2] WikiReading: A Novel Large-scale Language Understanding Task over Wikipedia Hewlett et al. 2016
    """
    def __init__(self, triples_file):
        self.annotator_name = "NoSubject-Triple-aligner"

        # load triples in memory
        d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")
                d["%s\t%s" % (tmp[0].strip(), tmp[2].strip())].append(tmp[1])

        # pd.read_csv(triples_file, sep="\t", names=["subject", "predicate", "object"]).set_index(['subject', 'object'])

        self.wikidata_triples = d

    def run(self, document):
        """
        :param: input document to align its sentences with triples
        :return:
        """
        #document.triples = []
        for sid, (start, end) in enumerate(document.sentences_boundaries):

            # Getting sentence subject
            # Every sentence has main entity as subject

            # if subject already tagged use it if not use only the URI
            # entities in sentence
            es = [j for j in document.entities if j.boundaries[0] >= start and j.boundaries[1] <= end]
            e_sub = [j for j in es if j.uri == document.uri]
            if len(e_sub) > 0:
                subject = e_sub[0]
            else:
                subject = Entity(document.uri,
                                 boundaries=None,
                                 surfaceform=document.title,
                                 annotator=self.annotator_name)

            for o in es:

                predicates = self.wikidata_triples["%s\t%s" % (subject.uri, o.uri)]

                for pred in predicates:
                    pred = Entity(pred, boundaries=None, surfaceform=None, annotator=self.annotator_name)

                    triple = Triple(subject=subject,
                                    predicate=pred,
                                    object=o,
                                    sentence_id=sid,
                                    annotator=self.annotator_name
                                    )

                    document.triples.append(triple)

        return document


class SimpleAligner(BasePipeline):
    """
    Take a document with tagged entities and match them with one another.
    Example : If we have three entities Q1, Q2 and Q3, it will try to find a
    property binding Q1 with Q2, Q2 with Q1, Q2 with Q3 etc...
    It won't match Q1 with itself, but if Q1 == Q2, it will try to find a
    property between them
    """
    def __init__(self, triples_file):
        """
        :param: input document containing the triples (two entities and
        the property that bind them together)
        """
        self.annotator_name = "Simple-Aligner"

        # load triples in memory
        d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")
                d["%s\t%s" % (tmp[0].strip(), tmp[2].strip())].append(tmp[1])

        self.wikidata_triples = d

    def run(self, document):
        """
        :param: input document to align its sentences with triples
        :return:
        """
        #document.triples = []
        for sid, (start, end) in enumerate(document.sentences_boundaries):

            es = [j for j in document.entities if j.boundaries[0] >= start and j.boundaries[1] <= end]

            # We use permutations to match every entity with all the others
            for o in itertools.permutations(es, 2):

                # We grab the predicates
                predicates = self.wikidata_triples["%s\t%s" % (o[0].uri, o[1].uri)]

                # And create the triples
                for pred in predicates:
                    pred = Entity(pred, boundaries=None, surfaceform=None, annotator=self.annotator_name)

                    triple = Triple(subject=o[0],
                                    predicate=pred,
                                    object=o[1],
                                    sentence_id=sid,
                                    annotator=self.annotator_name
                                    )

                    document.triples.append(triple)

        return document


class SPOAligner(BasePipeline):

    def __init__(self, triples_file):
        self.annotator_name = "SPOAligner"
        # Add here the name of the annotators creating entities with something else than properties
        self.annotator_list = ["Wikidata_Spotlight_Entity_Linker", "Simple_Coreference"]

        # load triples in memory
        d = defaultdict(list)
        with open(triples_file) as f:
            for l in f:
                tmp = l.split("\t")
                d["%s\t%s" % (tmp[0].strip(), tmp[2].strip())].append(tmp[1])

        self.wikidata_triples = d

    def run(self, document):
        document.triples = []
        for sid, (start, end) in enumerate(document.sentences_boundaries):

            # Entities created by the Entity linkers and the Coreference
            es = [j for j in document.entities if j.boundaries[0] >= start
                                                and j.boundaries[1] <= end
                                                and j.annotator in self.annotator_list]

            # Entities created by the Property Linker
            # uri [1:-1] to get rid of the < > surrounding the uri.
            p = [j.uri[1:-1] for j in document.entities if j.boundaries[0] >= start
                                                and j.boundaries[1] <= end
                                                and j.annotator == 'Wikidata_Property_Linker']

            for o in itertools.permutations(es, 2):
                predicates = self.wikidata_triples["%s\t%s" % (o[0].uri, o[1].uri)]
                # And create the triples
                for pred in predicates:
                    if pred[:-1] in p:  # [:-1] to remove the final c from the comparison
                        predic = Entity(pred, boundaries=None, surfaceform=None, annotator=self.annotator_name)

                        triple = Triple(subject=o[0],
                                        predicate=predic,
                                        object=o[1],
                                        sentence_id=sid,
                                        annotator=self.annotator_name
                                        )

                        document.triples.append(triple)

        return document

from pipeline import *
from collections import defaultdict

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
        :param: input document to align it's sentences with triples
        :return:
        """
        document.triples = []
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
                subject = Entity(document.uri, boundaries=None, surfaceform=document.title, annotator=self.annotator_name)

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


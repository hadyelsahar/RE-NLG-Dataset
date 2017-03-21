from pipeline import *
import pandas as pd

class NoSubjectAlign(BasePipeline):
    """
    Following the assumption in NoSUB  [1] and [2] that sentences in one paragraph all share the same subject.
    [1] Augenstein, Isabelle, Diana Maynard, and Fabio Ciravegna. "Distantly supervised web relation extraction for knowledge base population." Semantic Web 7.4 (2016): 335-349.
    [2] WikiReading: A Novel Large-scale Language Understanding Task over Wikipedia Hewlett et al. 2016
    """
    def __init__(self, triples_file):
        self.annotator_name = "NoSubject-Triple-aligner"
        # load triples in memory
        self.triples = pd.read_csv(triples_file, sep="\t", names=["subject", "predicate", "object"])

    def run(self, document):
        """
        :param: input document to align it's sentences with triples
        :return:
        """

        for sid, (start, end) in enumerate(document.sentences_boundaries):

            # Getting sentence subject
            # Every sentence has main entity as subject

            # if subject already tagged use it if not use only the URI
            # entities in sentence
            es = [j for j in document.entities if j.boundaires[0] >= start and j.boundaires[1] <= end]
            e_sub = [j for j in es if j.uri == document.uri]
            if e_sub > 0:
                subject = e_sub[0]
            else:
                subject = Entity(document.uri, boundaries=None, surfaceform=document.title, annotator=self.annotator_name)

            for o in es:

                predicates = self.triples[self.triples.subject == subject.uri][self.triples.object == o.uri].predicate.values

                for pred in predicates:

                    triple = Triple(subject=subject,
                                    predicate=pred,
                                    object=o,
                                    sentence_id=sid,
                                    annotator=self.annotator_name
                                    )

                    document.triples.append(triple)

        return document


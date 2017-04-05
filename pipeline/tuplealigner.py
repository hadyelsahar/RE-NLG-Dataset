
from pipeline import *
from entitylinker import *
from collections import defaultdict

class TupleAligner(BasePipeline):

    annotator_name = "tuple-aligner"


    def run(self, document):
        """
        :param: input document to align it's sentences with triples
        :return:
        """
        document.tuples = []

        for sid, (start, end) in enumerate(document.sentences_boundaries):

            # Getting sentence subject
            # Every sentence has main entity as subject

            entities = [i for i in document.entities if i.annotator == WikidataSpotlightEntityLinker.annotator_name and i.boundaries[0] >= start and i.boundaries[1] <= end]
            properties = [i for i in document.entities if i.annotator == POSPatternLinker.annotator_name and i.boundaries[0] >= start and i.boundaries[1] <= end]

            for e in entities:
                for p in properties:

                for pred in predicates:
                    pred = Entity(pred, boundaries=None, surfaceform=None, annotator=self.annotator_name)

                    triple = Tuple(subject=subject,
                                    predicate=pred,
                                    sentence_id=sid,
                                    annotator=self.annotator_name
                                    )

                    document.triples.append(triple)

        return document

    def get_dependency(self):


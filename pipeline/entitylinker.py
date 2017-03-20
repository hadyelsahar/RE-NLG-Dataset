from pipeline import  *
import spotlight

class DBpediaSpotlightEntityLinker(BasePipeline):

    def __init__(self, spotlight_url='http://localhost:2222/rest/annotate', confidence=0.2, support=1):
        """
        :param spotlight_url: url of the dbpedia spotlight service
        :param confidence: min confidence
        :param support:  min supporting document
        """
        self.annotator_name = 'DBpedia_spotlight'
        self.spotlight_url = spotlight_url
        self.confidence = confidence
        self.support = support

    def run(self, document):
        """
        :param document: Document object
        :return: Document after being annotated
        """

        document.entities = []

        for sid, (start, end) in enumerate(document.sentences_boundaries):

            try:
                annotations = spotlight.annotate(self.spotlight_url, document.text[start:end], self.confidence, self.support)

            except Exception as e:
                annotations = []

            for ann in annotations:

                e_start = document.sentences_boundaries[sid][0] + ann['offset']
                e_end = e_start + len(ann['surfaceForm'])

                entity = Entity(ann['URI'],
                       boundaries=(e_start, e_end),
                       surfaceform=ann['surfaceForm'],
                       annotator=self.annotator_name)

                document.entities.append(entity)

        return document



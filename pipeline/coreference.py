
from pipeline import *


class SimpleCoreference(BasePipeline):
    """
    a class for simple coreference
    to replace all pronouns with the base class uri
    """
    def __init__(self):
        self.annotator_name = 'Simple_Coreference'

    def run(self, document):
        """
        :param document: Class Document. Document containing
        :return:
        """
        # todo: fill in by pavlos
        # get base class URI   document.uri

        list_pronouns = ["he", "she", "it", "they"]

        for sid, (start, end_s) in enumerate(document.sentences_boundaries):
            for num, (x, y) in enumerate(document.words_boundaries):
                if x == start:
                    end_w = y
                    break

            if document.text[start:end_w].lower() in list_pronouns:
                entity = Entity(document.uri,
                                boundaries=(start, end_w),
                                surfaceform=document.title,
                                annotator=self.annotator_name)

                document.entities.append(entity)

        return document

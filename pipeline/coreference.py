
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

        list_pronouns = ["he", "she", "it", "they"]

        for sid, (start, end_s) in enumerate(document.sentences_boundaries):
            # Get the boundaries of the word in the beginning of the sentence
            for num, (x, y) in enumerate(document.words_boundaries):
                if x == start:
                    end_w = y
                    break
            # If this word is a pronoun found on the list above, create an entity with the URI of the document.
            if document.text[start:end_w].lower() in list_pronouns:
                entity = Entity(document.uri,
                                boundaries=(start, end_w),
                                surfaceform=document.text[start:end_w],
                                annotator=self.annotator_name)

                document.entities.append(entity)

        return document

from pipeline import *
import spotlight
import pandas as pd

class DBSpotlightEntityLinker(BasePipeline):

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

                if type(ann['surfaceForm']) not in [str, unicode]:
                    ann['surfaceForm'] = str(ann['surfaceForm'])

                e_end = e_start + len(ann['surfaceForm'])

                entity = Entity(ann['URI'],
                       boundaries=(e_start, e_end),
                       surfaceform=ann['surfaceForm'],
                       annotator=self.annotator_name)

                document.entities.append(entity)

        return document


class DBSpotlightEntityAndTypeLinker(BasePipeline):
    """
    Since DBpedia spotlight only tag resources not types
    for example the sentence :
    Berlin was the capital of the Kingdom of Prussia
    will get you the <http://dbpedia.org/resource/Capital_city> not the <http://dbpedia.org/ontology/Capital>
    so we can't map it to the triple
    <http://dbpedia.org/resource/Berlin> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Capital> .
    This Entity linker tries to alleviate that by searching is the resource matches a DBpedia ontology class
    """

    def __init__(self, dbo_file, dict_file, spotlight_url='http://localhost:2222/rest/annotate', confidence=0.2, support=1):
        """
        :param dbo_file:  file path containing all valid dbpedia classes, default ./datasets/dbpedia/dbpedia-classes.txt
        :param spotlight_url: url of the dbpedia spotlight service
        :param confidence: min confidence
        :param support:  min supporting document
        """
        self.annotator_name = 'DBpedia-spotlight-Entity-Type-Linker'
        self.spotlight_url = spotlight_url
        self.confidence = confidence
        self.support = support
        with open(dbo_file) as f:
            self.dbo_classes = set([i.strip() for i in f.readlines()])


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

                if type(ann['surfaceForm']) not in [str, unicode]:
                    ann['surfaceForm'] = str(ann['surfaceForm'])

                e_end = e_start + len(ann['surfaceForm'])

                # give priority to Tag DBpedia classes if they are tagged.
                tmp = ann['URI'].replace("resource", "ontology")
                if tmp in self.dbo_classes:
                    ann['URI'] = tmp

                entity = Entity(ann['URI'],
                       boundaries=(e_start, e_end),
                       surfaceform=ann['surfaceForm'],
                       annotator=self.annotator_name)

                document.entities.append(entity)

        return document


class WikidataSpotlightEntityLinker(BasePipeline):

    def __init__(self, db_wd_mapping, spotlight_url='http://localhost:2222/rest/annotate', confidence=0.2, support=1):
        """
        :param db_wd_mapping: csv file name containing mappings between DBpedia URIS and Wikdiata URIS
        :param spotlight_url: url of the dbpedia spotlight service
        :param confidence: min confidence
        :param support:  min supporting document
        """
        self.annotator_name = 'Wikidata_Spotlight_Entity_Linker'
        self.spotlight_url = spotlight_url
        self.confidence = confidence
        self.support = support

        self.mappings = {}
        with open(db_wd_mapping) as f:
            for l in f.readlines():
                tmp = l.split("\t")
                self.mappings[tmp[0].strip()] = tmp[1].strip()


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

                if type(ann['surfaceForm']) not in [str, unicode]:
                    ann['surfaceForm'] = str(ann['surfaceForm'])

                e_end = e_start + len(ann['surfaceForm'])

                # change DBpedia URI to Wikidata URI
                if ann['URI'] in self.mappings:
                    ann['URI'] = self.mappings[ann['URI']]
                else:
                    continue

                entity = Entity(ann['URI'],
                       boundaries=(e_start, e_end),
                       surfaceform=ann['surfaceForm'],
                       annotator=self.annotator_name)

                document.entities.append(entity)

        return document



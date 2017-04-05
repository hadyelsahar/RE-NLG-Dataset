from pipeline import *
import spotlight
import pandas as pd
from utils.textmatch import string_matching_rabin_karp

class DBSpotlightEntityLinker(BasePipeline):

    annotator_name = 'DBpedia_spotlight'

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

        if document.entities is None:
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
    annotator_name = 'DBpedia-spotlight-Entity-Type-Linker'

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
        if document.entities is None:
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

    annotator_name = 'Wikidata_Spotlight_Entity_Linker'


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

        if document.entities is None:
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


class POSPatternLinker(BasePipeline):

    annotator_name = "PosPatternLinker"

    def __init__(self, patterns, annotator_name=None, longest_sequence=True, filter_annotator=None, filter_mode="intersection"):
        """

        :param patterns: list of patterns to tag  ["NN NP", "VB NN" ..etc]
        :param annotator_name: annotator_name to add to annotations
        :param longest_sequence: pick longest sequence pattern match
                for example if  both patterns "NN" and "NN NP" matches will return only "NN NP"
        :param filter_annotator:  filter intersection with other entities tagged by annotator
                                    [list of annotator names to filter]

        :param filter_mode:  ["intersection", "subset"] filter tagged entities which match with intersection of previous tagged entities on two modes
                                intersection:  if they overlap  "largest city in" will not be returned if "city" is tagged as a named entity
                                subset: only if they are subset of the named entity "President of" will not be returned is "The president of United States" is tagged as a named entity
        """

        self.patterns = patterns
        self.annotator_name = annotator_name if annotator_name is not None else "PosPatternLinker"
        self.longest_sequence = longest_sequence
        self.filter_annotator = filter_annotator if filter_annotator is not None else []
        self.filter_mode = filter_mode


    def run(self, document):
        """
        :param document: input document to extract all pos patterns sequences inside and tag them as entities.
        :return: document after annotation of entities that match the sequences
        """

        for sid, (start, end) in enumerate(document.sentences_boundaries):
            # for each sentence collect pos tags annotated and
            # reconstructing a text containing all pos tags to send to the string matching algorithm
            es = [j for j in document.entities if j.boundaries[0] >= start and j.boundaries[1] <= end and j.annotator == "corenlp_pos"]
            postags = [e.uri for e in es]
            # save pos tags positions in a dictionary called positions to get them later
            c = 0
            positions = {}
            for i, j in enumerate(postags):
                positions[c] = i
                c += (len(j) + 1)

            postags = " ".join(postags)

            detected_entities = []

            for pattern in self.patterns:

                matched_positions = string_matching_rabin_karp(postags, pattern)
                # print matched_positions

                for i in [x for x in matched_positions if x in positions]:

                    start_id = positions[i]
                    end_id = positions[i] + len(pattern.split())-1
                    start_offset = es[start_id].boundaries[0]
                    end_offset = es[end_id].boundaries[1]

                    # make sure the sum of entities pos tags matches patterns
                    # important to match cases where  pattern  "NN NN" will mistakenly match the pattern "NN NNP"
                    # todo: use (1 char)id for each pattern

                    if pattern.strip() == " ".join([es[i].uri for i in range(start_id, end_id+1)]).strip():

                        detected_entities.append(Entity(
                            uri=pattern,
                            surfaceform=document.text[start_offset:end_offset],
                            annotator=self.annotator_name,
                            boundaries=(start_offset, end_offset)
                        ))


            # filtering entities
            if len(self.filter_annotator) > 0:

                filterlist = [j for j in document.entities
                              if j.boundaries[0] >= start and j.boundaries[1] <= end if j.annotator in self.filter_annotator]

                detected_entities = self.filter_entities(detected_entities, filterlist, mode="intersection")

            if self.longest_sequence:
                detected_entities = self.filter_entities(detected_entities, detected_entities, mode="subset")

            document.entities += detected_entities

        return document

    def filter_entities(self, entities, filterlist, mode="intersection"):
        """
        :param entities: list of entities to filter
        :param filterlist: list of entities to filter against
        :param mode: ["intersection", "subset"]
        :return: list of filtered entities
        """
        filtered_list = []

        for e in entities:

            match = False

            for ea in filterlist:

                if POSPatternLinker.match(e, ea,  mode == "subset"):

                    match = True
                    break

            if not match:
                filtered_list.append(e)

        return filtered_list

    @staticmethod
    def match(x, y, subsets=False):
        """
        helper method to detect if one of the entities contains within the second
        :param x: entities to check [Class Entity Object]
        :param y: entities to check against  [Class Entity Object]
        :param subsets: if True detect only subset not intersection
        :return:  True if boundaries of x matches y
        """

        r1 = range(x.boundaries[0], x.boundaries[1])
        r2 = range(y.boundaries[0], y.boundaries[1])

        if subsets:
            # match is not a case of subset
            # important !! because we compare the entity with itself
            if r1 == r2:
                return False
            # return True in case of subsets
            if all(x in r2 for x in r1):
                return True

        else:
            if any(x in r2 for x in r1):
                return True

        return False


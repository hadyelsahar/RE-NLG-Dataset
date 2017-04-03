from pipeline import *
from utils.corenlpclient import CoreNlPClient
import csv

class DBpediaAbstractsDataReader:
    """
    class with a default read_documents functions that yields Document iterator
    """
    def __init__(self, dataset_file, db_wd_mapping=None):
        """

        :param dataset_file: path of the dataset file
        :param db_wd_mapping: if given the page-uri will be changed from the one in the dataset
        to be mapped using the mappings file given.
        """

        self.dataset_file = dataset_file

        if db_wd_mapping is not None:
            self.mappings = {}
            with open(db_wd_mapping) as f:
                print "loading DBpedia to Wikidata URI mappings..."

                for l in f.readlines():
                    tmp = l.split("\t")
                    self.mappings[tmp[0].strip()] = tmp[1].strip()

        else:
            self.mappings = None

    def read_documents(self):
        """
        function that yields iterator of documents, the URI of each document is the DBpedia URI
        """
        with open(self.dataset_file) as f:
            read = csv.reader(f, delimiter="\t")

            for l in read:
                # extraction of title from DBpedia URI
                title = l[0].replace("http://dbpedia.org/resource/", "").replace("_", " ")

                if self.mappings is not None:
                    if l[0] in self.mappings:
                        l[0] = self.mappings[l[0]]
                    else:
                        continue

                document = Document(
                    docid=l[0],
                    pageuri=l[0],
                    title=title,
                    text=l[1].decode('utf-8')
                )

                yield document



class DBpediaAbstractsDataReaderWithCoreNLP:
    """
        class with a default read_documents functions that yields Document iterator
        the class is customized to read the dbpedia abstracts function and pass it first through the stanford corenlp
        fill in sentences, word boundaries and POS tags.
    """

    def __init__(self, dataset_file, db_wd_mapping=None):
        """

        :param dataset_file: path of the dataset file
        :param db_wd_mapping: if given the page-uri will be changed from the one in the dataset
        to be mapped using the mappings file given.
        """

        self.dataset_file = dataset_file
        self.corenlp = CoreNlPClient(annotators=["tokenize", "ssplit", "pos"])

        if db_wd_mapping is not None:
            self.mappings = {}
            with open(db_wd_mapping) as f:
                print "loading DBpedia to Wikidata URI mappings..."

                for l in f.readlines():
                    tmp = l.split("\t")
                    self.mappings[tmp[0].strip()] = tmp[1].strip()

        else:
            self.mappings = None

    def read_documents(self):
        """
        function that yields iterator of documents, the URI of each document is the DBpedia URI
        """
        with open(self.dataset_file) as f:
            read = csv.reader(f, delimiter="\t")

            for l in read:
                # extraction of title from DBpedia URI
                title = l[0].replace("http://dbpedia.org/resource/", "").replace("_", " ")
                text = l[1]
                if self.mappings is not None:
                    if l[0] in self.mappings:
                        l[0] = self.mappings[l[0]]
                    else:
                        continue

                # corenlp preprocessing
                p = self.corenlp.annotate(text)

                entities = []

                for i, postag in enumerate(p.postags):

                    e = Entity(
                        boundaries=p.words_boudaries[i],
                        surfaceform=p.tokens[i],
                        uri=postag,
                        annotator="corenlp_pos_tagger"
                    )

                    entities.append(e)

                text = text.decode("utf-8")

                document = Document(
                    docid=l[0],
                    pageuri=l[0],
                    title=title,
                    text=text,
                    words_boundaries=p.words_boudaries,
                    sentence_boundaries=p.sentences_boudaries,
                    entities=entities
                )

                yield document

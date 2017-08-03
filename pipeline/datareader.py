from pipeline import *
import csv
import glob
import os
import json

class DBpediaAbstractsDataReader:
    """
    class with a default read_documents functions that yields Document iterator
    """
    def __init__(self, dataset_file, db_wd_mapping=None, skip=0):
        """

        :param dataset_file: path of the dataset file
        :param db_wd_mapping: if given the page-uri will be changed from the one in the dataset
        :param skip: skip the first n documents
        to be mapped using the mappings file given.
        """

        self.dataset_file = dataset_file
        self.skip = skip

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
        function that yields iterator of documents
        the URI of each document is the Knowledge base URI after being mapped
        """
        with open(self.dataset_file) as f:
            read = csv.reader(f, delimiter="\t")

            # skip the first lines
            for i in range(self.skip):
                read.next()

            for l in read:
                # extraction of title from DBpedia URI
                title = l[0].replace("http://dbpedia.org/resource/", "").replace("_", " ")

                if self.mappings is not None:
                    if l[0] in self.mappings:
                        l[0] = self.mappings[l[0]]
                    else:
                        continue

                # For the cases where Wikidata ID is in the DBpedia URI
                elif 'wikidata.dbpedia.org' in l[0]:
                    l[0] = l[0].replace("http://wikidata.dbpedia.org/resource/", "http://www.wikidata.org/entity/")

                document = Document(
                    docid=l[0],
                    pageuri=l[0],
                    title=title,
                    text=l[1].decode('utf-8')
                )

                yield document


class TRExDataReader:
    """
    a reader to feed documents from a preprepared documents T-REx dataset exported in json in order to add modifications.
    """

    def __init__(self, dataset_folder, db_wd_mapping=None, skip=0, titles=None):
        """
        :param dataset_folder: path of the dataset folder where all trex files are given as .json files
        :param db_wd_mapping: if given the page-uri will be changed from the one in the dataset
                              in practice the given trex dataset already in wikidata uris so mappings aren't needed
        :param skip: skip the first n documents
        :param titles: a path for a tab separated file containing information about which wikipedia documents to keep
          the tab separated file has to have a column called title
          example of a file https://github.com/hadyelsahar/RE-NLG-Dataset/blob/evaluation/crowdsourcing/GR7bQ7Ra.tsv
        to be mapped using the mappings file given.
        """

        files_paths = glob.glob(os.path.join(dataset_folder, "*.json"))
        # sorting according to last edit to make experiments reproducible
        self.dataset_files = sorted(files_paths, key=os.path.getmtime)

        self.skip = skip

        self.titles = None   # list of document titles to skip if provided
        if titles is not None:

            titles = pd.read_csv(titles, sep="\t")["title"].values
            self.titles = set([i.replace("_", " ") for i in titles])

        if db_wd_mapping is not None:
            self.mappings = {}
            with open(db_wd_mapping) as f:
                print "loading URI mappings files..."

                for l in f.readlines():
                    tmp = l.split("\t")
                    self.mappings[tmp[0].strip()] = tmp[1].strip()

        else:
            self.mappings = None


    def read_documents(self):
        """
        function that yields iterator of documents
        the URI of each document is the Knowledge base URI after being mapped
        """

        i = 0   # i is the global document counter
        for f in self.dataset_files:
            docs = json.load(open(f))

            for d in docs:

                i += 1

                # skip the first lines if self.skip is given
                if i < self.skip:
                    continue

                if self.titles is not None and d['title'] not in self.titles:
                    continue

                if self.mappings is not None:
                    if d['uri'] in self.mappings:
                        d['uri'] = self.mappings[d['uri']]
                    else:
                        continue

                document = Document.fromJSON(d)

                yield document







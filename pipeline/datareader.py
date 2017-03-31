from pipeline import *
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







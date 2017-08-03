

class PlaceholderTypeTagger:
    """
    this class reads entities linked in the document
    and ads an entity type for each given a list of entities
    """

    def __init__(self, types_file):
        """

        :param type_mappings_file: csv file [tab separated] containing each URI with its type
        """

        self.types_dict = {}
        with open(types_file) as f:
            print "loading types of entities ..."
            for l in f.readlines():
                tmp = l.split("\t")
                self.types_dict[tmp[0].strip()] = tmp[1].strip()

    def run(self, d):

        for e in d.entities:

            if e.uri in self.types_dict:
                e.type_placeholder = self.types_dict[e.uri]

        return d

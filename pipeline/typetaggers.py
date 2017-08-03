class PropertyTypeTagger:
    """
    Set the type of the entities to the property
    in the triple connecting it to the main entity
    """
    def run(self, document):
        for e in document.entities:
            # check that it's not the main entity of the document
            if e.uri == document.uri:
                continue
            for t in document.triples:
                # if it is the triple with the aligned entity in the text
                if e == t.object:
                    e.type_placeholder = t.object.predicate.uri
                    break
                elif e == t.subject:
                    e.type_placeholder = t.subject.predicate.uri
                    break
                # if it is the triple that has the same entity id as subject or object
                elif e.uri == t.object.uri:
                    e.type_placeholder = t.object.predicate.uri
                elif e.uri == t.subject.uri:
                    e.type_placeholder = t.subject.predicate.uri
        return document

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

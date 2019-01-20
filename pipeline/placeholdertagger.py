class PropertyPlaceholderTagger:
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
                if e == t.object or e == t.subject:
                    e.property_placeholder = t.predicate.uri
                    break
                # if it is the triple that has the same entity id as subject or object
                elif e.uri == t.object.uri or e.uri == t.subject.uri:
                    e.property_placeholder = t.predicate.uri
        return document

class TypePlaceholderTagger:
    """
    this class reads entities linked in the document
    and ads an entity type for each given a list of entities
    """

    def __init__(self, types_file):
        """

        :param type_mappings_file: csv file [tab separated] containing each URI with its type
        """

        self.date_placeholder = "date"

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

            if "date" in e.annotator.lower():
                e.type_placeholder = self.date_placeholder

        return d

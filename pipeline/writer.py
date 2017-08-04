from pipeline import *
import json
import pickle
import os

class JsonWriter(BasePipeline):

    def __init__(self, outputfolder, basefilename=None, filesize=10000, startfile=0):
        """
        when attached to the pipeline this file log all json
        :param outputfolder: folder to save output files in
        :param basefilename: filename prefix to add before all file names
        :param filesize:
        """

        self.outputfolder = outputfolder

        if not os.path.exists(outputfolder):
            os.makedirs(outputfolder)

        self.basefilename = basefilename
        self.filesize = filesize
        self.counter = 0 + startfile
        self.buffer = []

    def run(self, document):

        self.counter += 1
        self.buffer.append(document.toJSON())

        if self.counter % self.filesize == 0:
            self.flush()

        return document

    def flush(self):
        
        filename = "%s-%s.json" % (self.counter-self.filesize, self.counter)
        filename = "%s_%s" % (self.basefilename, filename) if self.basefilename is not None else filename
        filename = os.path.join(self.outputfolder, filename)

        with open(filename, 'w') as outfile:
            json.dump(self.buffer, outfile)
            print "Saved file %s" % filename
            del self.buffer
            self.buffer = []

class CustomeWriterTriples(JsonWriter):
    def __init__(self, outputfolder, basefilename=None, filesize=10000, startfile=0):
        #super(CostumeWriterTriples, self).__init__(outputfolder, basefilename, filesize, startfile)
        JsonWriter.__init__(self, outputfolder, basefilename, filesize, startfile)
    def run(self, document):
        self.counter += 1
        triples = self.createTriples(document)

        self.buffer.append(triples)

        if self.counter % self.filesize == 0:
            self.flush()

        return document

    def createTriples(self, document):
        triples = {}
        triples['triples'] = []
        triples['additionalTriples'] = []
        triples['summary'] = document.text

        for t in document.triples:
            # check if main enitity of document is subject or object in the triple
            if t.subject.uri == document.docid:
                str_triple = t.subject.uri + ' ' + t.predicate.uri + ' ' + t.object.uri
                triples['triples'].append(str_triple)

            elif t.object.uri == document.docid:
                str_triple = t.subject.uri + ' ' + t.predicate.uri + ' ' + t.object.uri
                triples['additionalTriples'].append(str_triple)

        return triples

    def flush(self):
        filename = "%s-%s-triples.pkl" % (self.counter-self.filesize, self.counter)
        filename = "%s_%s" % (self.basefilename, filename) if self.basefilename is not None else filename
        filename = os.path.join(self.outputfolder, filename)

        with open(filename, 'w') as outfile:
            pickle.dump(self.buffer, outfile)
            print "Saved file %s" % filename
            del self.buffer
            self.buffer = []

class CustomeWriterEntities(JsonWriter):
    def __init__(self, outputfolder, basefilename=None, filesize=10000, startfile=0):
        JsonWriter.__init__(self, outputfolder, basefilename, filesize, startfile)

    def run(self, document):
        self.counter += 1
        entities = self.createEntities(document)

        self.buffer.append(entities)

        if self.counter % self.filesize == 0:
            self.flush()

        return document

    def createEntities(self, document):
        entities = []

        for e in document.entities:
            entity = {}
            entity['URI'] = e.uri
            entity['offset'] = e.boundaries[0]
            entity['surfaceForm'] = e.surfaceform
            entity['propertyplaceholder'] = e.property_placeholder
            entity['typeplaceholder'] = e.type_placeholder
            entity['annotator'] = e.annotator
            entities.append(entity)

        return entities

    def flush(self):
        filename = "%s-%s-entities.pkl" % (self.counter-self.filesize, self.counter)
        filename = "%s_%s" % (self.basefilename, filename) if self.basefilename is not None else filename
        filename = os.path.join(self.outputfolder, filename)

        with open(filename, 'w') as outfile:
            pickle.dump(self.buffer, outfile)
            print "Saved file %s" % filename
            del self.buffer
            self.buffer = []









from pipeline import *
import json
import os

class NIFWriter(BasePipeline):

    def __init__(self, outputfolder, basefilename=None, filesize=10000, startfile=0):
        """
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

        filename = "%s-%s.ttl" % (self.counter-self.filesize, self.counter)
        filename = "%s_%s" % (self.basefilename, filename) if self.basefilename is not None else filename
        filename = os.path.join(self.outputfolder, filename)
        with open(filename, 'w') as outfile:
            
            outfile.write("@prefix ann: <http://triplr.dbpedia.org/resource/> .")
            outfile.write("\n")
            outfile.write("@prefix wd: <http://www.wikidata.org/entity/> .")
            outfile.write("\n")
            outfile.write("@prefix wdt: <http://www.wikidata.org/prop/direct/> .")
            outfile.write("\n")
            outfile.write("@prefix nif: <http://ontology.neuinfo.org/NIF/Backend/nif_backend.owl#> .")
            outfile.write("\n")
            outfile.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
            outfile.write("\n")
            outfile.write("@prefix owl:  <http://www.w3.org/2002/07/owl#> .")
            outfile.write("\n")
            outfile.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
            outfile.write("\n")
            outfile.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
            outfile.write("\n")
            outfile.write("@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .")
            outfile.write("\n\n\n")

            for k in self.buffer:
                doccompleteuri = k['uri']
                docuri = doccompleteuri.split("/")[4]
                doc = "<" + doccompleteuri
                outfile.write(doc + "?nif=context>\n")
                outfile.write("\tnif:beginIndex " + '"0"^^xsd:nonNegativeInteger' + ";\n")
                outfile.write('\tnif:endIndex "' + str(len(k['text'])) + '"^^xsd:nonNegativeInteger' + ";\n")

                outfile.write('\tnif:isString """' + k['text'].encode('utf-8').replace('"','\\"') + '""" ;\n')
                outfile.write("\tnif:predLang <http://lexvo.org/id/iso639-3/eng> ;\n")
                outfile.write("\ta nif:Context .")
                outfile.write("\n\n\n")

                for c, j in enumerate(k['triples']):

                    pred = "wdt:" + j['predicate']['uri'].split("/")[5]

                    if j['subject']['annotator'] == 'Date_Linker':
                        subj = '"' + j['subject']['uri'].split("^^")[0] + '"^^<' + j['subject']['uri'].split("^^")[1] + ">"
                    else:
                        subj = "wd:" + j['subject']['uri'].split("/")[4]

                    if j['object']['annotator'] == 'Date_Linker':
                        obj = '"' + j['object']['uri'].split("^^")[0] + '"^^<' + j['object']['uri'].split("^^")[1] + ">"
                    else:
                        obj = "wd:" + j['object']['uri'].split("/")[4]

                    outfile.write("ann:" + str(c) + " a nif:AnnotationUnit ;\n")

                    outfile.write("\tnif:subject " + subj + " ;\n")
                    outfile.write("\tnif:predicate " + pred + " ;\n")
                    outfile.write("\tnif:object " + obj + " ;\n")
                    outfile.write('\trdfs:comment "' + j['annotator'] + '" .')
                    outfile.write("\n\n")

                    if j['annotator'] == "SPOAligner" or j['annotator'] == "Simple-Aligner":
                        if j['subject']['boundaries'] is not None:
                            boundaries_s = (j['subject']['boundaries'][0],j['subject']['boundaries'][1])
                        else:
                            boundaries_s = (0,0)

                        outfile.write(doc + "?nif=phrase&char=" + str(boundaries_s[0]) + "," + str(boundaries_s[1]) + ">\n")
                        outfile.write("\tnif:annotationUnit ann:annotation" + str(c) + " ;\n")
                        outfile.write('\tnif:anchorOf "' + j['subject']['surfaceform'].encode('utf-8') + '" ;\n')
                        outfile.write('\tnif:beginIndex "' + str(boundaries_s[0]) + '"^^xsd:nonNegativeInteger ;\n')
                        outfile.write('\tnif:endIndex "' + str(boundaries_s[1]) + '"^^xsd:nonNegativeInteger ;\n')
                        outfile.write("\tnif:referenceContext " + doc + "?nif=context> ;\n")
                        outfile.write("\titsrdf:taIdentRef " + subj + " ;\n")
                        outfile.write("\ta nif:Phrase ;\n")
                        outfile.write('\trdfs:comment "' + j['subject']['annotator'] + '" .')
                        outfile.write("\n\n")

                        if j['annotator'] == "SPOAligner":
                    
                            if j['predicate']['boundaries'] is not None:   
                                boundaries_p = (j['predicate']['boundaries'][0],j['predicate']['boundaries'][1])
                            else:
                                boundaries_p = (0,0)                        

                            outfile.write(doc + "?nif=phrase&char=" + str(boundaries_p[0]) + "," + str(boundaries_p[1]) + ">\n")
                            outfile.write("\tnif:annotationUnit ann:annotation" + str(c) + " ;\n")
                            outfile.write('\tnif:anchorOf "' + j['predicate']['surfaceform'].encode('utf-8') + '" ;\n')
                            outfile.write('\tnif:beginIndex "' + str(boundaries_p[0]) + '"^^xsd:nonNegativeInteger ;\n')
                            outfile.write('\tnif:endIndex "' + str(boundaries_p[1]) + '"^^xsd:nonNegativeInteger ;\n')
                            outfile.write("\tnif:referenceContext " + doc + "?nif=context> ;\n")
                            outfile.write("\titsrdf:taIdentRef " + pred + " ;\n")
                            outfile.write("\ta nif:Phrase ;\n")
                            outfile.write('\trdfs:comment "' + j['predicate']['annotator'] + '" .')
                            outfile.write("\n\n")

                    
                    if j['object']['boundaries'] is not None:
                        boundaries_o = (j['object']['boundaries'][0],j['object']['boundaries'][1])
                    else:
                        boundaries_o = (0,0)


                    outfile.write(doc + "?nif=phrase&char=" + str(boundaries_o[0]) + "," + str(boundaries_o[1]) + ">\n")
                    outfile.write("\tnif:annotationUnit ann:annotation" + str(c) + " ;\n")
                    outfile.write('\tnif:anchorOf "' + j['object']['surfaceform'].encode('utf-8') + '" ;\n')
                    outfile.write('\tnif:beginIndex "' + str(boundaries_o[0]) + '"^^xsd:nonNegativeInteger ;\n')
                    outfile.write('\tnif:endIndex "' + str(boundaries_o[1]) + '"^^xsd:nonNegativeInteger ;\n')
                    outfile.write("\tnif:referenceContext " + doc + "?nif=context> ;\n")
                    outfile.write("\titsrdf:taIdentRef " + obj + " ;\n")
                    outfile.write("\ta nif:Phrase ;\n")
                    outfile.write('\trdfs:comment "' + j['object']['annotator'] + '" .')
                    outfile.write("\n\n\n\n")

            print "Saved file %s" % filename
            del self.buffer
            self.buffer = []
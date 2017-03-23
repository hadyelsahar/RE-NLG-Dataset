from pipeline import *
import json
import os

class JsonWriter(BasePipeline):

    def __init__(self, outputfolder, basefilename=None, filesize=10000):
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
        self.counter = 0
        self.buffer = []

    def run(self, document):

        self.counter += 1
        self.buffer.append(document.toJSON())
        print len(self.buffer)

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
            self.buffer = []






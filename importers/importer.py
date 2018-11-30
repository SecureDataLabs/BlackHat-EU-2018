from events import *
from writers import *

class importer(object):
    def __init__(self, event, writer, args):
        self.event = event
        self.ouputwriter = writer(args)
        self.timeformat = args.timeformat
        self.args = args

    def processFile(self, filename):
        raise Exception("Not implemented in base class")

    def saveEvent(self, event):
        self.ouputwriter.saveEvent(event)
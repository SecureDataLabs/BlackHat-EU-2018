import argparse
from writers.writer import writer

filename = None

class csv_filewriter(writer):
    def __init__(self, args):
        super(csv_filewriter, self).__init__(args)
        self.outfile = open(filename, "w")

    def saveEvent(self, event):
        self.outfile.write("{}\n".format(event.toCSV(self.args.timeformat)))
        
    def doneWriting(self):
        self.outfile.close()

def getClass():
    return csv_filewriter

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--outfile", help="Filename/Location of the CSV output file", required=True)
(moduleargs, extra) = parser.parse_known_args()
filename = moduleargs.outfile
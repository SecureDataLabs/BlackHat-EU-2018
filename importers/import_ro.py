import csv
import argparse
import sys
from importers.importer import importer

app = None

class roimpoter(importer):
    def processFile(self, filename):
        lineCount = 0
        print("Starting processing now")
        with open(filename, "r", encoding="utf-8") as fo:
            datareader = csv.reader(fo, delimiter=",")
            for l in datareader:
                if lineCount == 0:
                    lineCount += 1
                    continue
                e = self.event(timeformat=self.timeformat)
                e.setTimestamp(l[0], timeformat=self.timeformat)
                e.setEntity(l[1])
                e.setEventclass(l[2])
                e.setSourceIp(l[3])
                e.setDestinationIp(l[5])
                e.setDestinationPort(l[6])
                self.saveEvent(e)
                   
def getClass():
    return roimpoter

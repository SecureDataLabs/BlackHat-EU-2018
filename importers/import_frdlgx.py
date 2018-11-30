import csv
import argparse
import sys
from importers.importer import importer

app = None

class frdlgximporter(importer):
    def processFile(self, filename):
        lineCount = 0
        print("Starting frdlgx processing now")
        with open(filename, "r", encoding="utf-8") as fo:
            datareader = csv.reader(fo, delimiter=",")
            for l in datareader:
                if lineCount == 0:
                    lineCount += 1
                    continue
                ip = l[0]
                # Skip IPv6 addresses
                if ':' in ip:
                    continue
                e = self.event(timeformat=self.timeformat)
                e.setEntity('frdlgx')
                e.setSeverity(l[1])
                e.setEventclass("AIE: Network Anomaly: Ext : Threat List IP - Allow")
                e.setSourceIp(l[0])
                self.saveEvent(e)

def getClass():
    return frdlgximporter
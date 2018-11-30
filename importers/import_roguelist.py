import csv
import argparse
import sys
from importers.importer import importer

app = None

class roguelistimporter(importer):
    def processFile(self, filename):
        lineCount = 0
        print("Starting roguelist processing now")
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
                datetime = '{date} 00:00:00'.format(date=l[1])
                e.setTimestamp(datetime, timeformat=self.timeformat)
                e.setEntity('rougelist')
                e.setSeverity(l[5])
                e.setEventclass("AIE: Network Anomaly: Ext : Threat List IP - Allow")
                e.setSourceIp(l[2])
                self.saveEvent(e)

def getClass():
    return roguelistimporter
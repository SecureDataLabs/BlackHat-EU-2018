import json
import argparse
import sys
from importers.importer import importer

app = None

class mhnimporter(importer):
    def processFile(self, filename):
        with open(filename, encoding="utf-8") as fo:
            for l in fo:
                doc = json.loads(l)
                if doc["_source"]["log"]["app"] == app:
                    e = self.event(timeformat=self.timeformat)
                    if doc['_source']['log']["tcp_len"] == "null":
                        e.setProtocol("UDP")
                    e.setTimestamp(doc["_source"]["log"]["timestamp"], timeformat=self.timeformat)
                    e.setSeverity(doc['_source']['log']["severity"])
                    e.setDirection(doc['_source']['log']["direction"])
                    e.setEntity(doc['_source']['beat']["hostname"])
                    e.setSourceType(doc['_source']['log']["ids_type"])
                    e.setEventtype(doc["_source"]["log"]["type"])
                    e.setSignature(doc["_source"]["log"]["signature"])
                    e.setSourceIp(doc["_source"]["log"]["src_ip"])
                    e.setDestinationIp(doc["_source"]["log"]["dest_ip"])
                    e.setDestinationPort(doc["_source"]["log"]["dest_port"])
                    self.saveEvent(e)
                else:
                    continue

def getClass():
    return mhnimporter

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--app", help="Import only data from this app source, eg snort", required=True)
(moduleargs, extra) = parser.parse_known_args()
app = moduleargs.app
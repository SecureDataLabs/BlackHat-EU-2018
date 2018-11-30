import json
import sys
import argparse
from importlib import import_module
from events.mhnevent import mhnevent
from datetime import datetime
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="The file to import")
parser.add_argument("-t", "--timeformat", help="Python style timestamp format string, eg '%Y-%m-%dT%H:%M:%S.%f'", default="%Y-%m-%dT%H:%M:%S.%f")
parser.add_argument("-w", "--writer", help="The output writer module to use", required=True)
parser.add_argument("-e", "--eventtype", help="The event type module to use", required=True)
parser.add_argument("-i", "--input", help="The input processor module to use", required=True)
(args, extra) = parser.parse_known_args()



inputFile = args.filename
tsFormat = args.timeformat     

if __name__=="__main__":
    # Changing the import string to start with 'importers.' works, else we observe a runtime error. 
    # Why the subsequent import_module strings work is not clear.
    importer = import_module("importers." + args.input).getClass()
    writer = import_module("." + args.writer, package="writers").getClass()
    event = import_module("." + args.eventtype, package="events").getClass()

    i = importer(event, writer, args)
    i.processFile(args.filename)
    i.ouputwriter.doneWriting()
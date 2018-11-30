from datetime import datetime
from events.token_map import *
from events.rule_map import *
 
class event(object):
    def __init__(self, timeformat="%Y-%m-%dT%H:%M:%S.%f"):
        self._timestamp = None
        self._protocol = "TCP"
        self._severity = None
        self._direction = None
        self._app = None
        self._entity = None
        self._sourcetype = None
        self._eventclass = None
        self._eventtype = None
        self._signature = None
        self._sourceip = None
        self._destinationip = None
        self._destinationport = None
        self._rawmessage = None
        self._batchname = None
        self._batchtag = None
        self._key = None
        self._token = None

    def setTimestamp(self, timestring, timeformat):
        self._timestamp = datetime.strptime(timestring, timeformat)

    def setProtocol(self, protocol):
        self._protocol = protocol

    def setSeverity(self, severity):
        self._severity = severity

    def setDirection(self, direction):
        self._direction = direction

    def setEntity(self, entity):
        if entity in token_map:
            self._entity = "{} {} {}".format(token_map[entity][0], token_map[entity][1], token_map[entity][2])
        else:
            self._entity = entity

    def setSourceType(self, sourceType):
        self._sourcetype = sourceType
    
    def setEventclass(self, eventClass):
        if eventClass in rule_map:
            self._eventclass = rule_map[eventClass]
        else:
            self._eventclass = eventClass

    def setEventtype(self, eventType):
        self._eventtype = eventType

    def setSignature(self, signature):
        self._signature = signature

    def setSourceIp(self, sourceIp):
        self._sourceip = sourceIp

    def setDestinationPort(self, destinationport):
        if destinationport == "":
            destinationport = None
        self._destinationport = destinationport

    def setDestinationIp(self, destinationip):
        self._destinationip = destinationip

    def setBatchName(self, batchname):
        self._batchname = batchname

    def setBatchTag(self, batchtag):
        self._batchtag = batchtag

    def setKey(self, key):
        self._key

    def setToken(self, token):
        self._token

    def toCSV(self, timeformat):
        return "{},{},{},{},{},{},{},{},{},{},{},{},{}".format(self._timestamp.strftime(timeformat),
            self._app,
            self._severity, 
            self._protocol,
            self._direction,
            self._entity,
            self._sourcetype,
            self._eventtype,
            self._eventclass,
            self._signature,
            self._sourceip,
            self._destinationip,
            self._destinationport)

    def toSQL(self):
        raise Exception("Not implemented")
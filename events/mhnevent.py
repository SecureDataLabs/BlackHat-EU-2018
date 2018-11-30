from events.event import event
from events.rule_map import *

class mhnevent(event):
    def __init__(self, timeformat="%Y-%m-%dT%H:%M:%S.%f"):
        super(mhnevent, self).__init__(timeformat="%Y-%m-%dT%H:%M:%S.%f")
        self._eventclass = rule_map["AIE: SD: External IPS high severity Alert"]


def getClass():
    return mhnevent
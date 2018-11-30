class writer(object):
    def __init__(self, args):
        self.args = args

    def saveEvent(self, event):
        raise Exception("Not implemented")

    def doneWriting(self):
        raise Exception("Not implemented")
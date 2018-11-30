import psycopg2
import argparse
from writers.writer import writer

createTableSQL = """CREATE TABLE public.event_data{}
(
   id serial, 
   "timestamp" timestamp without time zone, 
   protocol text, 
   severity text, 
   direction text, 
   app text, 
   entity text, 
   sourcetype text, 
   eventclass text, 
   sourceip text, 
   destinationip text, 
   destinationport integer, 
   rawmessage text, 
   batchname text, 
   batchtag text, 
   CONSTRAINT pk_id_{} PRIMARY KEY (id)
) 
WITH (
  OIDS = FALSE
)
;
"""

insertEventSQL = """INSERT INTO public.event_data{}(
            "timestamp", protocol, severity, direction, app, entity,
            sourcetype, eventclass, sourceip, destinationip, destinationport, 
            rawmessage, batchname, batchtag)
    VALUES (%s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s);
"""

checkTableExist = "SELECT 'public.event_data{}'::regclass"
moduleargs = None

class pg_writer(writer):
    _batchsize = 10000
    _batchcounter = 0
    def __init__(self, args):
        super(pg_writer, self).__init__(args)
        self.conn = psycopg2.connect(host=moduleargs.host,database=moduleargs.database, user=moduleargs.username, password=moduleargs.password, port=moduleargs.port)
        self.cur = self.conn.cursor()
        try:
            #self. checking it table exists
            self.cur.execute("SELECT 'public.event_data{}'::regclass".format(moduleargs.tablepostfix))
        except Exception as ex:
            print(ex)
            print("Table event_data{} not found, creating".format(moduleargs.tablepostfix))
            self.conn.rollback()
            self.cur.execute(createTableSQL.format(moduleargs.tablepostfix, moduleargs.tablepostfix))
            self.conn.commit()
            print("Table event_data{} created".format(moduleargs.tablepostfix))

    def saveEvent(self, event):
        self._batchcounter += 1
        sql = insertEventSQL.format(moduleargs.tablepostfix)
        self.cur.execute(sql, (event._timestamp, event._protocol, event._severity, event._direction, event._app, event._entity,
            event._sourcetype, event._eventclass, event._sourceip, event._destinationip, event._destinationport, event._rawmessage,
            event._batchname, event._batchtag))
        if self._batchcounter >= self._batchsize:
            self._batchcounter = 0
            self.conn.commit()

    def doneWriting(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        

def getClass():
    return pg_writer

parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", help="The postgres database server you want to connect to", default="localhost")
parser.add_argument("-p", "--port", help="The postgres database server port you want to connect to", default=5432)
parser.add_argument("-D", "--database", help="The postgres database you want to connect to", required=True)
parser.add_argument("-U", "--username", help="The postgres username you want to connect as", required=True)
parser.add_argument("-P", "--password", help="The password for the database user", required=True)
parser.add_argument("-T", "--tablepostfix", help="An optional table postfix to use a different table", default="")
(moduleargs, extra) = parser.parse_known_args()
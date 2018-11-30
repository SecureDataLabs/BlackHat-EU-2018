import psycopg2
import argparse
import prepare_insert_into

suffix_list = ["lt5m", "lt5m_honeyserver", "lt5m_no_ro", "5mtolt48h", "5mtolt48h_honeyserver", "5mtolt48h_no_ro", "first48h", "first48h_honeyserver", "first48h_no_ro", "48htolt7d", "48htolt7d_honeyserver", "48htolt7d_no_ro", "7dormore", "7dormore_honeyserver", "7dormore_no_ro"]

create_table_template = """
CREATE TABLE public.event_data_{table_suffix} 
(
	id serial NOT NULL,
	orig_sourceip text NULL,
	"orig_timestamp" timestamp NULL,
	orig_eventclass text NULL,
	orig_entity text NULL,
	"match_timestamp" timestamp NULL,
	match_eventclass text NULL,
	match_entity text NULL,
	match_destinationip text NULL,
	match_destinationport int4 NULL,
	timedelta int4 null,
	CONSTRAINT pk_id__event_data_{table_suffix} PRIMARY KEY (id)
)
;"""
idx_orig_timestamp = """CREATE INDEX event_data_import_{table_suffix}_orig_timestamp_idx ON public.event_data_{table_suffix} (orig_timestamp);"""
idx_orig_entity = """CREATE INDEX event_data_import_{table_suffix}_orig_entity_idx ON public.event_data_{table_suffix} (orig_entity);"""
idx_orig_sourceip = """CREATE INDEX event_data_import_{table_suffix}_orig_sourceip_idx ON public.event_data_{table_suffix} (orig_sourceip);"""
idx_timedelta = """CREATE INDEX event_data_import_{table_suffix}_timedelta_idx ON public.event_data_{table_suffix} (timedelta);"""

def create_tables(conn, cur, suffix_list):
    for suffix in suffix_list:
        try:
            cur.execute("SELECT 'public.event_data_{}'::regclass".format(suffix))
        except Exception as ex:
            conn.rollback()
            cur.execute(create_table_template.format(table_suffix=suffix))
            conn.commit()

def create_table_idx(conn, cur, suffix_list):
    for suffix in suffix_list:
        try:
            sql = idx_orig_timestamp.format(table_suffix=suffix)
            cur.execute(sql)
            sql = idx_orig_entity.format(table_suffix=suffix)
            cur.execute(sql)
            sql = idx_orig_sourceip.format(table_suffix=suffix)
            cur.execute(sql)
            sql = idx_timedelta.format(table_suffix=suffix)
            cur.execute(sql)
            conn.commit()
        except Exception as ex:
            print(ex)
            conn.rollback()
            print('Aborting Index Creation!!!!')
            break

def do_prepare(moduleags):
    conn = psycopg2.connect(host=moduleargs.host,database=moduleargs.database, user=moduleargs.username, password=moduleargs.password, port=moduleargs.port)
    cur = conn.cursor()
    create_tables(conn, cur, suffix_list)

    print('Going to prepare Event Data less than 5 minutes, excluding "honeyserver" entities on the matching set')
    cur.execute(prepare_insert_into.insert_event_data_lt5m)
    conn.commit()
    print('Going to prepare Event Data less than 5 minutes only looking at "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_lt5m_honeyserver)
    conn.commit()
    print('Going to prepare Event Data less than 5 minutes excluding "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_lt5m_no_ro)
    conn.commit()

    print('Going to prepare Event Data equal to or greather than 5 minutes and less than 48 hours, excluding "honeyserver" entities on the matching set')
    cur.execute(prepare_insert_into.insert_event_data_5mtolt48h)
    conn.commit()
    print('Going to prepare Event Data equal to or greather than 5 minutes and less than 48 hours only looking at "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_5mtolt48h_honeyserver)
    conn.commit()
    print('Going to prepare Event Data equal to or greather than 5 minutes and less than 48 hours excluding "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_5mtolt48h_no_ro)
    conn.commit()
    
    print('Going to prepare Event Data for this first 48 hours, excluding "honeyserver" entities on the matching set')
    cur.execute(prepare_insert_into.insert_event_data_first48h)
    conn.commit()
    print('Going to prepare Event Data for this first 48 hours only looking at "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_first48h_honeyserver)
    conn.commit()
    print('Going to prepare Event Data for this first 48 hours excluding "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_first48h_no_ro)
    conn.commit()
    
    print('Going to prepare Event Data equal to or greather than 48 hours and less than 7 days, excluding "honeyserver" entities on the matching set')
    cur.execute(prepare_insert_into.insert_event_data_48htolt7d)
    conn.commit()
    print('Going to prepare Event Data equal to or greather than 48 hours and less than 7 days, only looking at "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_48htolt7d_honeyserver)
    conn.commit()
    print('Going to prepare Event Data equal to or greather than 48 hours and less than 7 days, excluding "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_48htolt7d_no_ro)
    conn.commit()
 
    print('Going to prepare Event Data 7 days or more, excluding "honeyserver" entities on the matching set')
    cur.execute(prepare_insert_into.insert_event_data_7dormore)
    conn.commit()
    print('Going to prepare Event Data 7 days or more looking at "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_7dormore_honeyserver)
    conn.commit()
    print('Going to prepare Event Data 7 days or more excluding "honeyservers" on the original set, matching everything excluding "repeat offenders"')
    cur.execute(prepare_insert_into.insert_event_data_7dormore_no_ro)
    conn.commit()

    create_table_idx(conn, cur, suffix_list)

    cur.close()
    conn.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="The postgres database server you want to connect to", default="localhost")
    parser.add_argument("-p", "--port", help="The postgres database server port you want to connect to", default=5432)
    parser.add_argument("-D", "--database", help="The postgres database you want to connect to", required=True)
    parser.add_argument("-U", "--username", help="The postgres username you want to connect as", required=True)
    parser.add_argument("-P", "--password", help="The password for the database user", required=True)
    (moduleargs, extra) = parser.parse_known_args()
    do_prepare(moduleargs)
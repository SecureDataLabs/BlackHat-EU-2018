import psycopg2
import argparse
import hashlib

base_table_name = 'event_data_{}'
suffix_list = ["import"]

check_if_colmn_exists = """SELECT count(column_name) FROM information_schema.columns WHERE table_name=%s and column_name=%s;
"""
alter_table_add_column = """ALTER TABLE {} ADD {} text NULL;
"""
get_non_transformed_col = """SELECT * FROM {table_name} WHERE (newsourceip is NULL or newdestinationip is NULL) and id > {last_id} order by id limit {record_limit};
"""
update_transformed_col = """update {table_name} set newsourceip = %s, newdestinationip = %s where id = %s;
"""

def prep_add_column(cur, table_suffix, column_name):
    result = False
    row = None
    altertable_add_col = False
    cur.execute(check_if_colmn_exists, (base_table_name.format(table_suffix), column_name))
    row = cur.fetchone()
    if row:
        if row[0] == 0:
            altertable_add_col = True

    if altertable_add_col:
        sql = alter_table_add_column.format(base_table_name.format(table_suffix), column_name)
        cur.execute(sql)
        # The column was added
        result = True
    return result

def add_required_columns(conn, cur):
    added_any = False
    for suffix in suffix_list:
        added_newsourceip = prep_add_column(cur, suffix, 'newsourceip')
        added_newdestinationip = prep_add_column(cur, suffix, 'newdestinationip')
        added_any = added_newsourceip or added_newdestinationip
    if added_any:
        conn.commit()

def create_update(cur, rows, table_name, salt):
    last_id = -1
    update_rows = []
    for row in rows:
        id = row[0]
        if id > last_id:
            last_id = id
        sourceip = row[9]
        destinationip = row[10]
        update_rows.append([id, sourceip, destinationip])
        
    for update_row in update_rows:
        id = update_row[0]
        oldsourceip = update_row[1]
        if oldsourceip:
            sha_1 = hashlib.sha1()
            update_value = '{salt}{value}'.format(salt=salt,value=oldsourceip)
            sha_1.update(update_value.encode('utf-8'))
            newsourceip = sha_1.hexdigest()
        else:
            newsourceip = None

        olddestinationip = update_row[2]
        if olddestinationip:
            sha_1 = hashlib.sha1()
            update_value = '{salt}{value}'.format(salt=salt,value=olddestinationip)
            sha_1.update(update_value.encode('utf-8'))
            newdestinationip = sha_1.hexdigest()
        else:
            newdestinationip = None

        sql = update_transformed_col.format(table_name=table_name)
        cur.execute(sql, (newsourceip, newdestinationip, id))
    return last_id

def transform_columns(conn, cur, table_name, salt, batch_size):
    done = False
    last_id = 0
    while not done:
        sql = get_non_transformed_col.format(table_name=table_name, last_id=last_id, record_limit=batch_size)
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            end_id = create_update(cur, rows, table_name, salt)
            print("Updated {table_name} Record Range ID: {start_id} - {end_id}".format(table_name=table_name, start_id=last_id, end_id=end_id))
            last_id = end_id
            conn.commit()
        else:
            done = True

def restructure_table(conn, cur, table_suffix):
    drop_index = "DROP INDEX public.event_data_{suffix}_sourceip_idx;".format(suffix=table_suffix)
    drop_sourceip = "ALTER TABLE public.event_data_{suffix} DROP COLUMN sourceip;".format(suffix=table_suffix)
    drop_destinationip = "ALTER TABLE public.event_data_{suffix} DROP COLUMN destinationip;".format(suffix=table_suffix)
    rename_sourceip = "ALTER TABLE public.event_data_{suffix} RENAME COLUMN newsourceip TO sourceip;".format(suffix=table_suffix)
    rename_destinationip = "ALTER TABLE public.event_data_{suffix} RENAME COLUMN newdestinationip TO destinationip;".format(suffix=table_suffix)
    create_index = "CREATE INDEX event_data_{suffix}_sourceip_idx ON public.event_data_import (sourceip);".format(suffix=table_suffix)
    
    cur.execute(drop_index)
    cur.execute(drop_sourceip)
    cur.execute(drop_destinationip)
    cur.execute(rename_sourceip)
    cur.execute(rename_destinationip)
    cur.execute(create_index)
    conn.commit()

def do_transform_columns(conn, cur, salt, batch_size):
    for suffix in suffix_list:
        transform_columns(conn, cur, base_table_name.format(suffix), salt, batch_size)
        restructure_table(conn, cur, suffix)

def do_prepare(moduleags):
    conn = psycopg2.connect(host=moduleargs.host,database=moduleargs.database, user=moduleargs.username, password=moduleargs.password, port=moduleargs.port)
    cur = conn.cursor()
    try:
        add_required_columns(conn, cur)
        do_transform_columns(conn, cur, moduleags.salt, moduleags.batch_size)
    except Exception as ex:
        print(ex)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", help="The postgres database server you want to connect to", default="localhost")
    parser.add_argument("-p", "--port", help="The postgres database server port you want to connect to", default=5432)
    parser.add_argument("-D", "--database", help="The postgres database you want to connect to", required=True)
    parser.add_argument("-U", "--username", help="The postgres username you want to connect as", required=True)
    parser.add_argument("-P", "--password", help="The password for the database user", required=True)
    parser.add_argument("-S", "--salt", help="The salt that will be used with the value to hide the original value.", required=True)
    parser.add_argument("-B", "--batch_size", help="The batch size.", default=5000)
    (moduleargs, extra) = parser.parse_known_args()
    do_prepare(moduleargs)
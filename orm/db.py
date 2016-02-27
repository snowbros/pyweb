import psycopg2
from tools.config import config_options
connection = False


def _get_connection():
    global connection
    if not connection or connection.closed:
        connection = psycopg2.connect("dbname='%s' user='batsy'"%(config_options.db_name))
    return connection

def _get_cursor():
    con = _get_connection()
    return con.cursor()

def _commit():
    con = _get_connection()
    con.commit()

def _execute_query(query_string, values={}):
    cursor = _get_cursor()
    cursor.execute(query_string, values)
    return cursor


#database select operation
#    *query_string: full query type = string
#    *values: field values type = dict
def select_all(query_string, values):
    cursor = _execute_query(query_string, values)
    rows = cursor.fetchall()
    return rows
def select_one(query_string, values):
    cursor = _execute_query(query_string, values)
    return cursor.fetchone()

#is table already exist or not 
#TODO: replace with cr.execute("SELECT relname FROM pg_class WHERE relkind in ('r','v') AND relname=%s", (table_name,))
def _table_exist(table_name):
    result = select_one("select exists(select relname from pg_class where relname=%(table_name)s)", {"table_name": table_name})
    return result[0]

#for creating table
def _create_table(table_name):
    if not _table_exist(table_name):
        _execute_query('CREATE TABLE "%s" (id SERIAL NOT NULL, PRIMARY KEY(id)) WITH OIDS'%(table_name,))
        _commit()
    return True

#fields realated methods
def _orm_get_columns_info(model_obj):
    table_name =  model_obj._table_name
    fields = model_obj._fields.keys()
    fields.append('id')
    result = select_all("""SELECT c.relname,a.attname,a.attlen,a.atttypmod,a.attnotnull,a.atthasdef,t.typname,CASE WHEN a.attlen=-1 THEN a.atttypmod-4 ELSE a.attlen END as size
        FROM pg_class c,pg_attribute a,pg_type t
        WHERE c.relname=%s
        AND a.attname in %s
        AND c.oid=a.attrelid 
        AND a.atttypid=t.oid""", (table_name, tuple(fields)))
    field_info = {}
    for r in result:
        field_info[r[1]] = {'table_name': r[0], 'field_name': r[1], 'data_type':r[-2], 'size':r[-1]}
    return field_info

def _orm_add_column(field_obj, size=False):
    table_name = field_obj._table_name
    field_name = field_obj._field_name
    f_type = field_obj._type
    if size:
        _execute_query('ALTER TABLE "%s" ADD COLUMN "%s" %s(%s)'%(table_name, field_name, f_type, field_size))
    else:
        _execute_query('ALTER TABLE "%s" ADD COLUMN "%s" %s'%(table_name, field_name, f_type))
    _commit()

#for inserting data into table
def _insert_data(table_name, column_name , column_type):
    if _table_exist(table_name):
        column_data = raw_input("enter data")
        
        try:
            assert column_type in ["INT","VARCHAR2","DATE","BOOLEAN",]
            _execute_query("INSERT INTO %s (%s) VALUES (%s);"%(table_name,column_name,column_data))
            _commit()
        except AssertionError:
            print "invalid data type"
    else:
        print "table not exists"
def _retrive_data(table_name, column_name):
    if _table_exist(table_name):
        
        result = select_all("SELECT %s FROM %s;"%(column_name, table_name), {"column_name": column_name, "table_name": table_name,})
        print result
    
    else:
        print "table not exists"

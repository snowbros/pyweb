import psycopg2

connection = False


def _get_connection():
    global connection
    if not connection or connection.closed:
        connection = psycopg2.connect("dbname='test' user='batsy'")
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
def _table_exist(table_name):
    result = select_one("select exists(select relname from pg_class where relname=%(table_name)s)", {"table_name": table_name})
    return result[0]

#for creating table
def _create_table(table_name):
    if not _table_exist(table_name):
        _execute_query("CREATE TABLE %s (id INT PRIMARY KEY)"%(table_name,))
        _commit()
    return True


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

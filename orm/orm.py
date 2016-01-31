import db

class ORM(object):
    def __init__(self):
        table_name =  self._table_name
        db._create_table(table_name)

        for f in self._fields:
            pass
            #logic for adding column
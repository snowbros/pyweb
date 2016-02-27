import db
import logging

logger = logging.getLogger(__name__)

class ORM(object):

    _auto_mode = True

    def __init__(self):
        if self._auto_mode:
            self._auto_init()


    def _auto_init(self):
        table_name =  self._table_name
        db._create_table(table_name)

        field_list =  db._orm_get_columns_info(self)
        for f_name, f_obj in self._fields.items():
            f_obj._set_meta(table_name, f_name)
            if f_name not in field_list:
                f_obj._add_column()

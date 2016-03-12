import db
import logging
from conditions import Parser

logger = logging.getLogger(__name__)


class ORM(object):

    _auto_mode = True

    def __init__(self):
        if self._auto_mode:
            self._auto_init()

    def _auto_init(self):
        table_name = self._table_name
        db._create_table(table_name)

        field_list = db._orm_get_columns_info(self)
        for f_name, f_obj in self._fields.items():
            f_obj._set_meta(table_name, f_name)
            if f_name not in field_list:
                f_obj._add_column()
        self._field_dict = db._orm_get_columns_info(self)

    def prepare_query(self, values):

        fields, vals = [], []
        all_fields = self._field_dict.keys()
        for field_name, value in values.items():
            if field_name in all_fields:
                fields.append(field_name)
                vals.append(value)
            else:
                logger.warning("Skipped, Field '%s' not available" % (field_name))
        return tuple(fields), tuple(vals)

    def create(self, values):
        fields, vals = self.prepare_query(values)
        db._insert_data(self._table_name, fields, vals)

    def write(self, list_id, values):
        fields, vals = self.prepare_query(values)
        db._update_data(self._table_name, fields, vals, list_id)

    def delete(self, list_id):
        db._delete_data(self._table_name, list_id)

import db
import logging
from conditions import Parser

logger = logging.getLogger(__name__)


class TableRegistry:

    class __TableRegistry:
        table_registry = {}

        def _add_table_entry(self, table_obj):
            self.table_registry[table_obj._table_name] = table_obj

        def __getattr__(self, name):
            if self.table_registry.get(name):
                return self.table_registry.get(name)
            else:
                raise AttributeError

    instance = None

    def __init__(self):
        if not TableRegistry.instance:
            TableRegistry.instance = TableRegistry.__TableRegistry()

    def add_table_entry(self, table_obj):
        self.instance._add_table_entry(table_obj)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        if self.instance is None:
            return "TableRegistry(No Init)"
        else:
            return "TableRegistry() with %s" % (TableRegistry.instance.table_registry.keys())


class ORM(object):

    _auto_mode = True
    Registry = TableRegistry()

    def __init__(self):
        if self._auto_mode:
            self._auto_init()
        self.Registry.add_table_entry(self)

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

    def generate_where_clause(self, conditions):
        try:
            where_clause = Parser(self, conditions)._to_sql_str()
        except AssertionError as e:
            logger.error(e)
            return False
        return where_clause

    def search(self, conditions, order='id', offset=0, limit=""):
        where_clause = self.generate_where_clause(conditions)
        return db._get_ids(self._table_name, where_clause, order, offset, limit)

    def search_read(self, conditions, fields=None, order='id', offset=0, limit=""):
        all_fields = self._field_dict.keys()
        if not fields:
            fields = all_fields
        else:
            fields = [f for f in fields if f in all_fields]
        where_clause = self.generate_where_clause(conditions)
        return db._get_vals_dict(self._table_name, where_clause, fields, order, offset, limit)

    def read(self, ids, fields=None, order='id', offset=0, limit=""):
        all_fields = self._field_dict.keys()
        if not fields:
            fields = all_fields
        else:
            fields = [f for f in fields if f in all_fields]
        if ids:
            domain = [['id', 'in', tuple(ids)]]
        else:
            domain = []
        where_clause = self.generate_where_clause(domain)
        print where_clause
        return db._get_vals_dict(self._table_name, where_clause, fields, order, offset, limit)

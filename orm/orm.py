import db
import logging
from conditions import Parser

from fields import ForeignKeys

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


class M2OGetter(object):

    def __init__(self, model, ref_model, id):
        self.model = model
        self.ref_model = ref_model
        self.id = id

    def _get(self):
        # To-do: replace read with search read if it is safe
        if not self.id:
            return {}
        # To-do: Replace this hack [self.id, 0]
        return getattr(self.model.Registry, self.ref_model).read([self.id])[0]


class ORM(object):

    _auto_mode = True
    Registry = TableRegistry()

    def __init__(self):
        self.M2Os = []
        if self._auto_mode:
            self._auto_init()
        self.Registry.add_table_entry(self)
        if not ForeignKeys._table_registry:
            ForeignKeys._table_registry = TableRegistry()
        ForeignKeys.generate_foreign_keys()

    def _auto_init(self):
        table_name = self._table_name
        db._create_table(table_name)

        field_list = db._orm_get_columns_info(self)
        for f_name, f_obj in self._fields.items():
            f_obj._set_meta(table_name, f_name)
            if f_name not in field_list:
                f_obj._add_column()
            if f_obj._real_type == "M2O":
                self.M2Os.append(f_name)
        self._field_dict = db._orm_get_columns_info(self)

    def prepare_query(self, values):

        fields, vals = [], []
        all_fields = self._field_dict.keys()
        for field_name, value in values.items():
            if field_name in all_fields:
                fields.append(field_name)
                if type(value) is unicode:
                    vals.append(value.encode('utf-8'))
                else:
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

    def get_relational_result(self, result, relational_fields):

        for i, res in enumerate(result):
            for relational_field in relational_fields:
                ref_model = self._fields[relational_field]._ref_model
                result[i][relational_field] = M2OGetter(self, ref_model, res.get(relational_field))
        return result

    def search_read(self, conditions, fields=None, order='id', offset=0, limit=""):
        all_fields = self._field_dict.keys()
        if not fields:
            fields = all_fields
        else:
            fields = [f for f in fields if f in all_fields]
        where_clause = self.generate_where_clause(conditions)
        result = db._get_vals_dict(self._table_name, where_clause, fields, order, offset, limit)

        relational_fields = [f for f in self.M2Os if f in result[0].keys()]
        if relational_fields:
            self.get_relational_result(result, relational_fields)

        return result

    def search_read_basic(self, conditions, fields=None, order='id', offset=0, limit=""):
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
        if len(ids) > 1:
            domain = [['id', 'in', tuple(ids)]]
        elif ids:
            domain = [['id', '=', ids[0]]]
        else:
            domain = []
        where_clause = self.generate_where_clause(domain)
        return db._get_vals_dict(self._table_name, where_clause, fields, order, offset, limit)

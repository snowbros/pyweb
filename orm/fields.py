import db
import logging

logger = logging.getLogger(__name__)


class BaseField(object):

    _type = None
    _table_name = None
    _field_name = None

    def __init__(self, **args):
        self._size = None

    def set(self, cr, obj, id, name, value, user=None, context=None):
        cr.execute('update '+obj._table+' set '+name+'='+self._symbol_set[0]+' where id=%s', (self._symbol_set[1](value), id))

    def get(self, cr, obj, ids, name, user=None, offset=0, context=None, values=None):
        raise Exception('undefined get method !')

    def _set_meta(self, table_name, field_name):
        self._table_name = table_name
        self._field_name = field_name

    def _add_column(self):
        logger.error("You need to implement this method")


class Text(BaseField):

    _type = "text"
    _real_type = "text"

    def _add_column(self):
        db._orm_add_column(self)


class Char(BaseField):

    _type = "varchar"
    _real_type = "char"

    def __init__(self, size=256, **args):
        self._size = size

    def _add_column(self):
        db._orm_add_column(self)


class Integer(BaseField):

    _type = "INT"
    _real_type = "int"

    def _add_column(self):
        db._orm_add_column(self)


class Float(BaseField):
    _type = "numeric"
    _real_type = "float"

    def _add_column(self):
        db._orm_add_column(self)


class Boolean(BaseField):
    _type = "bool"
    _real_type = "boolean"

    def _add_column(self):
        db._orm_add_column(self)


class Date(BaseField):
    _type = "date"
    _real_type = "date"

    def _add_column(self):
        db._orm_add_column(self)


class Date_time(BaseField):
    _type = "timestamp"
    _real_type = "datetime"

    def _add_column(self):
        db._orm_add_column(self)


class Binary(BaseField):

    _type = "bytea"
    _real_type = "binary"

    def _add_column(self):
        db._orm_add_column(self)


class ManyToOne(BaseField):

    _type = "INT"
    _real_type = "M2O"

    def __init__(self, model, **args):
        self._size = None
        self._ref_model = model
        ForeignKeys(self)

    def _add_column(self):
        db._orm_add_column(self)


class ForeignKeys(object):

    _keys_map = {}
    _table_registry = False

    def __init__(self, field):
        if self._keys_map.get(field._ref_model):
            self._keys_map.get(field._ref_model).append(field)
        else:
            self._keys_map[field._ref_model] = [field]

    @staticmethod
    def generate_foreign_keys():
        for model, fields in ForeignKeys._keys_map.items():
            if hasattr(ForeignKeys._table_registry, model):
                for field in fields:
                    db._add_foreign_key(field)
                del ForeignKeys._keys_map[model]

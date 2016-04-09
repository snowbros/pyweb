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

    def _add_column(self):
        db._orm_add_column(self)


class Char(BaseField):

    _type = "varchar"

    def __init__(self, size=256, **args):
        self._size = size

    def _add_column(self):
        db._orm_add_column(self)


class Integer(BaseField):

    _type = "INT"

    def _add_column(self):
        db._orm_add_column(self)


class Float(BaseField):
    _type = "numeric"

    def _add_column(self):
        db._orm_add_column(self)


class Boolean(BaseField):
    _type = "bool"

    def _add_column(self):
        db._orm_add_column(self)


class Date(BaseField):
    _type = "date"

    def _add_column(self):
        db._orm_add_column(self)


class Date_time(BaseField):
    _type = "timestamp"

    def _add_column(self):
        db._orm_add_column(self)


class Binary(BaseField):

    _type = "bytea"

    def _add_column(self):
        db._orm_add_column(self)

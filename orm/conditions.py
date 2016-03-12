import logging

logger = logging.getLogger(__name__)


class Condition(object):
    """It will used to hold one condition
    It will also verify operators, and parse values to stop SQL-Injection
        * Pass values like
            > ['name', '=', 'kishan']
            > ['amount', '>', 1223]
        * _to_sql_str() will convert it into
            > name = 'kishan'
            > amount = 123
        These strings are going to used in parser to build query
    """
    def __init__(self, field_name, operator, value, model):
        self.field_name = field_name
        self.operator = operator
        self.value = value
        self.is_valid = False   # not used for now
        self.model = model
        self._validate_expr()

    def _validate_expr(self):
        # TO-DO: If want to validate expression values is valid or not
        assert self.field_name in self.model._field_dict.keys(), "Field '%s' not in table '%s'" % (self.field_name, self.model._table_name)
        assert self.operator in ['=', '!=', '<>', '<', '>', '<=', '>=', 'in', 'like', 'ilike', 'not in'], "Wrong Operator '%s'" % (self.operator)
        if self.operator in ['in', 'not in']:
            assert isinstance(self.value, tuple), "If you use operator 'in' value should be tuple"
        self.is_valid = True

    def __str__(self):
        return "Condition(%s %s %s)" % (repr(self.field_name), repr(self.operator), repr(self.value))

    def __repr__(self):
        return "Condition(%s %s %s)" % (repr(self.field_name), repr(self.operator), repr(self.value))

    def _to_sql_str(self):
        return "%s %s %s" % (self.field_name, self.operator, repr(self.value))


class Parser(object):
    """Parser is used to convert in list type conditions in to SQL-where clause condition
    Most of the time it will called from search() of ORM
    It will convert this expression
        [['name', '=', 'kishan'], ['amount', '<', 1000], (['price', '=', 1000], 'or', ['price', '>', 100]), 'or', ['amount', '>', 100], 'and', ['price', '>', 1500]]
    into
        name = 'kishan' AND amount < 1000 AND (price = 1000 OR price > 100) OR amount > 100 AND price > 1500
    Rules:
        * condition should be 3 length list containing field name, operator and value
            > e.g. [['name', '=', 'kishan']]
        * If you put two condition, you can use AND/OR between conditions
            > e.g. [['name', '=', 'kishan'], 'OR', ['name', '=', 'kishan']]
        * by default if you don't put any thing it will considered as a AND
            > so [['name', '=', 'kishan'], ['name', '=', 'kishan']]
              will be [['name', '=', 'kishan'], 'AND', ['name', '=', 'kishan']]
        * If you want priorities in conditions put it between () tuple
            > [['name', '=', 'kishan'], (['price', '=', 1000], 'or', ['price', '>', 100])]
    """
    def __init__(self, model, expr):
        self.expr = expr
        self.model = model
        self.is_tuple = False
        self.sql_list = []
        if isinstance(expr, list):
            self._parse()
        elif isinstance(expr, tuple):
            self.is_tuple = True
            self._parse()
        else:
            assert False, "This part of condition %s  must be list/tuple" % (expr)

    def _parse(self):
        expr_len = len(self.expr) - 1
        for n, item in enumerate(self.expr):
            if n != 0 and not isinstance(self.expr[n-1], str) and not isinstance(item, str):
                self.sql_list.append('AND')
            if isinstance(item, list):
                if len(item) != 3:
                    assert False, "Wrong Condition Syntax: %s" % (item)
                cond = Condition(item[0], item[1], item[2], self.model)
                self.sql_list.append(cond._to_sql_str())
            elif isinstance(item, tuple):
                self.sql_list.append(Parser(self.model, item)._to_sql_str())
            elif isinstance(item, str):
                assert item.upper() in ["AND", "OR"], "Invalid Logical operator"
                if n == 0 or n == expr_len or not isinstance(self.expr[n-1], (list, tuple)) or not isinstance(self.expr[n+1], (list, tuple)):
                    assert False, "Operator At Wrong Place"
                else:
                    self.sql_list.append(item.upper())
            else:
                assert False, "Wrong Expression Syntax"

    def _to_sql_str(self):
        query = " ".join(self.sql_list)
        if self.is_tuple:
            query = "(%s)" % (query)
        return query

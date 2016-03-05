from orm import orm, fields


class Task(orm.ORM):
    _table_name = "task"

    _fields = {
        'name': fields.Text(),
        'name2': fields.Char(size=100)
    }

Task()

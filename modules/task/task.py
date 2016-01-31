from orm import orm


class Task(orm.ORM):
    _table_name = "task"

Task()

from orm import fields, orm


class Project(orm.ORM):
    _table_name = "project_main"

    _fields = {
        'name': fields.Char()
    }


Project()

# class Tasks(orm.ORM):
#     _table_name = "tasks"


# Tasks()
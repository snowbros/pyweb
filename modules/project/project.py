from orm import orm, fields

class Project(orm.ORM):
    _table_name = "projects"

    _fields = {
        'name': fields.Text(),
    }

Project()

# class Tasks(orm.ORM):
#     _table_name = "tasks"


# Tasks()
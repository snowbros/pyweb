from orm import orm, fields


class Project(orm.ORM):
    _table_name = "projects"

    _fields = {
        'name': fields.Char(),
        'color': fields.Char(),
        'description': fields.Text(),
        'archive': fields.Boolean(),
        'date': fields.Date_time()
    }

p = Project()

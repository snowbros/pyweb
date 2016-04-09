from orm import orm, fields


class Project(orm.ORM):
    _table_name = "projects"

    _fields = {
        'name': fields.Char(),
        'description': fields.Text(),
        'archive': fields.Boolean()
    }

p = Project()

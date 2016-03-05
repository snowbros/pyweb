from orm import orm, fields


class Project(orm.ORM):
    _table_name = "projects"

    _fields = {
        'name': fields.Text(),
    }

Project()

from orm import orm, fields


class Project(orm.ORM):
    _table_name = "projects"

    _fields = {
        'name': fields.Text(),
        'amount': fields.Integer(),
        'price': fields.Float(),
        'last_date': fields.Date(),
        'datetime': fields.Date_time(),
        'active': fields.Boolean()
    }

p = Project()

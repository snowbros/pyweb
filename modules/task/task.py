from orm import orm, fields


class Task(orm.ORM):
    _table_name = "tasks"

    _fields = {
        'name': fields.Char(),
        'color': fields.Char(),
        'description': fields.Text(),
        'archive': fields.Boolean(),
        'date': fields.Date_time(),
        'user_id': fields.ManyToOne('users'),
        'project_id': fields.ManyToOne('projects'),
        'date_deadline': fields.Date_time(),
        'state': fields.Char()
    }

Task()

from orm import orm, fields


class Users(orm.ORM):
    _table_name = "users"

    _fields = {
        'name': fields.Char(),
        'email': fields.Char(),
        'password_hash': fields.Char()
    }

Users()

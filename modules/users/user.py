from orm import orm


class Users(orm.ORM):
    _table_name = "users"

Users()

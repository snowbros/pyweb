from orm import orm


class Project(orm.ORM):
    _table_name = "projects"

    _fields = {
            'name': {
                        'type': 'VARCHAR2',
                        'not null': True
                    },
            'description': {
                        'type': 'VARCHAR2',
                    },
    }



Project()

# class Tasks(orm.ORM):
#     _table_name = "tasks"


# Tasks()
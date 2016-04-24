import json

from modules.flask_app import web
from flask import render_template, url_for
from flask.ext.login import login_required, current_user

from forms import TaskForm

from orm.orm import TableRegistry


table_registry = TableRegistry()


@web.route('/get_task_model', methods=('GET', 'POST'))
@web.route('/get_task_model/<int:record_id>', methods=('GET', 'POST'))
@login_required
def create_tasks(record_id=False):
    form = TaskForm()
    if form.validate_on_submit():
        values = {
            'name': form.name.data,
            'description': form.description.data,
            'color': form.color.data,
            'date': form.date.data,
            'user_id': form.user_id.data,
            'date_deadline': form.date_deadline.data,
            'state': form.state.data
        }
        if record_id:
            table_registry.tasks.write([record_id], values)
        else:
            table_registry.tasks.create(values)
        return json.dumps({'redirect': url_for('tasks')})
    elif record_id:
        project_data = table_registry.tasks.search_read([['id', '=', record_id]])[0]
        form.name.data = project_data['name']
        form.description.data = project_data['description']
        form.color.data = project_data['color']
        form.date.data = project_data['date'].strftime('%d/%m/%Y %I:%M %p')

    return render_template('backend/task_model.html', form=form, record_id=record_id and str(record_id))


# secure methods
@web.route('/tasks')
@login_required
def tasks():
    return render_template('backend/tasks.html', main_class='task_home')



@web.route('/autocomplete/users')
# @login_required
def users_list():
    user_data = []
    for user in table_registry.users.read([]):
        if user['name'] and user['id']:
            user_data.append({
                "value": user['name'],
                "data": str(user['id'])
                })
    return json.dumps(user_data)

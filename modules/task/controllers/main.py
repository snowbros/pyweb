import json

from modules.flask_app import web
from flask import render_template, url_for, request
from flask.ext.login import login_required, current_user

from forms import TaskForm

from orm.orm import TableRegistry


table_registry = TableRegistry()


@web.route('/get_task_model', methods=('GET', 'POST'))
@web.route('/get_task_model/<int:record_id>', methods=('GET', 'POST'))
@login_required
def create_tasks(record_id=False, **post):
    user = False
    project_id = request.args.get('project_id', 0, type=int)
    form = TaskForm()
    if project_id:
        form.project_id.data = project_id
    state = request.args.get('state', '', type=str)
    if project_id:
        form.state.data = state
    if form.validate_on_submit():
        values = {
            'name': form.name.data,
            'description': form.description.data,
            'color': form.color.data,
            'date': form.date.data,
            'user_id': form.user_id.data,
            'project_id': form.project_id.data,
            'date_deadline': form.date_deadline.data,
            'state': form.state.data
        }
        if record_id:
            table_registry.tasks.write([record_id], values)
        else:
            table_registry.tasks.create(values)
        return json.dumps({'redirect': url_for('tasks') + '/' + str(form.project_id.data)})
    elif record_id:
        project_data = table_registry.tasks.search_read([['id', '=', record_id]])[0]
        form.name.data = project_data['name']
        form.description.data = project_data['description']
        form.color.data = project_data['color']
        form.date.data = project_data['date'].strftime('%m/%d/%Y %I:%M %p')
        form.date_deadline.data = project_data['date_deadline'].strftime('%m/%d/%Y %I:%M %p')
        form.project_id.data = project_data['project_id']._get()['id']
        user = project_data['user_id']._get()
        form.user_id.data = user['id']
        form.state.data = project_data['state']

    return render_template('backend/task_model.html', form=form, record_id=record_id and str(record_id), user_name=user and user['name'] or "")


# secure methods
@web.route('/tasks')
@web.route('/tasks/<int:project_id>')
@login_required
def tasks(project_id=False):
    project = False
    if project_id:
        project = table_registry.projects.search_read([['id', '=', project_id]])[0]
        sub_domain = [['project_id', '=', project_id]]
    else:
        sub_domain = [['user_id', '=', current_user.data.get('id')]]

    search = request.args.get('search', '', type=str)
    if search:
        sub_domain.append(['name', 'ilike', "%%"+search+"%%"])

    tasks = {
        'new': table_registry.tasks.search_read([['state', '=', 'new']] + sub_domain),
        'progress': table_registry.tasks.search_read([['state', '=', 'progress']] + sub_domain),
        'test': table_registry.tasks.search_read([['state', '=', 'test']] + sub_domain),
        'done': table_registry.tasks.search_read([['state', '=', 'done']] + sub_domain)
    }
    return render_template('backend/tasks.html', main_class='task_home', tasks=tasks, project=project, search=search)


@web.route('/move_task/<int:task_id>/<state>')
@login_required
def move_task(task_id, state):
    table_registry.tasks.write([task_id], {'state': state})
    return json.dumps({'redirect': url_for('tasks')})


@web.route('/autocomplete/users')
@login_required
def users_list():
    user_data = []
    for user in table_registry.users.read([]):
        if user['name'] and user['id']:
            user_data.append({
                "value": user['name'],
                "data": str(user['id'])
                })
    return json.dumps(user_data)

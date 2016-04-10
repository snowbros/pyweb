import json

from modules.flask_app import web
from flask import render_template, url_for
from flask.ext.login import login_required, current_user

from forms import ProjectForm

from orm.orm import TableRegistry


table_registry = TableRegistry()


# secure methods
@web.route('/get_project_model', methods=('GET', 'POST'))
@web.route('/get_project_model/<int:record_id>', methods=('GET', 'POST'))
@login_required
def create_project(record_id=False):
    form = ProjectForm()
    if form.validate_on_submit():
        values = {
            'name': form.name.data,
            'description': form.description.data,
            'color': form.color.data,
            'date': form.date.data,
        }
        if current_user.data.get('id') and not record_id:
            values['user_id'] = current_user.data.get('id')
        if record_id:
            table_registry.projects.write([record_id], values)
        else:
            table_registry.projects.create(values)
        return json.dumps({'redirect': url_for('home')})
    elif record_id:
        project_data = table_registry.projects.search_read([['id', '=', record_id]])[0]
        form.name.data = project_data['name']
        form.description.data = project_data['description']
        form.color.data = project_data['color']
        form.date.data = project_data['date'].strftime('%d/%m/%Y %I:%M %p')

    return render_template('backend/project_model.html', form=form, record_id = record_id and str(record_id))


# secure methods
@web.route('/home')
@login_required
def home():
    projects = table_registry.projects.search_read([])
    return render_template('backend/home.html', main_class='project_home', projects=projects, current_user=current_user)

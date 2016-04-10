import json

from modules.flask_app import web
from flask import render_template, url_for
from flask.ext.login import login_required, current_user

from forms import ProjectForm

from orm.orm import TableRegistry


table_registry = TableRegistry()


# secure methods
@web.route('/get_project_model', methods=('GET', 'POST'))
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        values = {
            'name': form.name.data,
            'description': form.description.data,
            'color': form.color.data,
            'date': form.date.data,
        }
        if current_user.data.get('id'):
            values['user_id'] = current_user.data.get('id')
        table_registry.projects.create(values)
        return json.dumps({'redirect': url_for('home')})
    return render_template('backend/project_model.html', form=form)


# secure methods
@web.route('/home')
@login_required
def home():
    projects = table_registry.projects.search_read([])
    return render_template('backend/home.html', main_class='project_home', projects=projects)

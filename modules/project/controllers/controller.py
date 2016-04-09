import json

from modules.flask_app import web
from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from forms import ProjectForm

from orm.orm import TableRegistry


table_registry = TableRegistry()


# secure methods
@web.route('/get_project_model', methods=('GET', 'POST'))
# @login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        values = {
            'name': form.name.data,
            'description': form.description.data,
            'color': form.color.data,
            'date': form.date.data
        }
        table_registry.projects.create(values)
        return json.dumps({'redirect': url_for('home')})
    return render_template('backend/project_model.html', form=form)


# secure methods
@web.route('/home')
# @login_required
def home():
    projects = table_registry.projects.search_read([])
    return render_template('backend/home.html', main_class='project_home',projects=projects)


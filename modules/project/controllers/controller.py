from modules.flask_app import web
from flask import render_template, redirect, url_for
from flask.ext.login import login_required

from orm.orm import TableRegistry


table_registry = TableRegistry()


# secure methods
@web.route('/get_project_model', methods=('GET', 'POST'))
# @login_required
def create_project():
    return render_template('backend/project_model.html')

from modules.flask_app import web_path
from flask import render_template


@web_path.route('/login')
def login():
    return render_template('login.html', name="user")

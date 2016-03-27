from modules.flask_app import web_path
from flask import render_template


@web_path.route('/login')
def login():
    return render_template('login.html', main_class ="login_back")


@web_path.route('/')
def home():
    return render_template('home.html')

@web_path.route('/base')
def base():
    return render_template('base.html')

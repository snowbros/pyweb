from modules.flask_app import web
from flask import render_template


@web.route('/login')
def login():
    return render_template('login.html', main_class ="login_back")


@web.route('/')
def home():
    return render_template('home.html')

@web.route('/base')
def base():
    return render_template('base.html')

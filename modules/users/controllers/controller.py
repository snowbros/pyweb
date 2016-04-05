from modules.flask_app import web
from flask import render_template, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user
from werkzeug.security import generate_password_hash

from user_auth import UsersAuthenticator
from forms import LoginForm, SignUpForm
from orm.orm import TableRegistry


table_registry = TableRegistry()

login_manager = LoginManager()
login_manager.init_app(web)


def do_login(user_email, password):
    user = UsersAuthenticator(user_email)
    if user.exist:
        user.validate_user(password)
        if user.is_authenticated:
            login_user(user)
            return True
        else:
            return None
    return False


@web.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        state = do_login(form.email.data, form.password.data)
        if state:
            return redirect(url_for('home'))
        elif state is None:
            form.password.errors = ['Wrong Password']
        else:
            form.email.errors = ['User does not exist']
    form.password.data = None
    return render_template('login.html', main_class="login_back", form=form)


@web.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        user_data = {
            'name': sign_up_form.name.data,
            'password_hash': generate_password_hash(sign_up_form.password.data),
            'email': sign_up_form.email.data
        }
        table_registry.users.create(user_data)
        if do_login(sign_up_form.email.data, sign_up_form.password.data):
            return redirect(url_for('home'))

    sign_up_form.password.data = None
    sign_up_form.password_cmp.data = None
    return render_template('sign_up.html', main_class="login_back", form=sign_up_form)


@login_manager.user_loader
def load_user(user_id):
    user = UsersAuthenticator.get_user_obj(user_id)
    if user:
        return user
    return None


@web.route('/')
def index():
    return render_template('index.html')


@web.route('/home')
@login_required
def home():
    return render_template('home.html')


@web.errorhandler(401)
def no_auth(e):
    return redirect(url_for('login'))


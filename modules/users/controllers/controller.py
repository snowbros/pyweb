import json

from modules.flask_app import web
from flask import render_template, redirect, url_for
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash

from user_auth import UsersAuthenticator
from forms import LoginForm, SignUpForm, ChangepasswordForm, Edit_profile
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
    return render_template('login/login.html', main_class="login_back", form=form)


@web.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout_redirect'))


@web.route("/logout_redirect")
def logout_redirect():
    print "loggag"
    return redirect(url_for('index'))


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
    return render_template('login/sign_up.html', main_class="login_back", form=sign_up_form)


@web.route('/change_password', methods=('GET', 'POST'))
def change_password():
    change_pass_form = ChangepasswordForm()
    if change_pass_form.validate_on_submit():
        current_id = current_user.data.get('id')
        user_data = {
            'password_hash': generate_password_hash(change_pass_form.password.data)
        }
        table_registry.users.write([current_id], user_data)
        return json.dumps({'redirect': url_for('home')})
    return render_template('backend/change_password.html', form=change_pass_form)


@web.route('/edit_profile', methods=('GET', 'POST'))
def edit_profile():
    edit_profile_form = Edit_profile()
    if edit_profile_form.validate_on_submit():
        current_id = current_user.data.get('id')
        user_data = {
            'name': edit_profile_form.name.data,
            'email': edit_profile_form.email.data
        }
        table_registry.users.write([current_id], user_data)
        return json.dumps({'redirect': url_for('home')})
    return render_template('backend/edit_profile.html', form=edit_profile_form)


@login_manager.user_loader
def load_user(user_id):
    user = UsersAuthenticator.get_user_obj(user_id)
    if user:
        return user
    return None


@web.route('/')
def index():
    return render_template('frontend/home.html')


@web.errorhandler(401)
def no_auth(e):
    return redirect(url_for('login'))

from modules.flask_app import web
from flask import redirect, url_for, session
from flask.ext.login import login_user

from flask_oauth import OAuth
from user_auth import UsersAuthenticator

oauth = OAuth()

GOOGLE_CLIENT_ID = 'Yout client id'
GOOGLE_CLIENT_SECRET = 'your secret id'
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


@web.route('/google_login')
def google_login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@web.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    user = UsersAuthenticator(False, oauth_token=access_token)
    user.o_auth_validate()
    if user.is_authenticated:
        login_user(user)
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')

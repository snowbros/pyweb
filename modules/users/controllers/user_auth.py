import random
import time
import json


from orm.orm import TableRegistry
from werkzeug.security import check_password_hash

table_registry = TableRegistry()


class UsersAuthenticator(object):

    user_sessions = {}

    def __init__(self, email, oauth_token=False):
        self.exist = False
        self.oauth_varified = False
        if oauth_token and not email:
            self.oauth_data = self.get_google_user_info(oauth_token)
            if self.oauth_data and self.oauth_data.get('email'):
                email = self.oauth_data.get('email')
                self.oauth_create_user()
        user_table = table_registry.users
        user = user_table.search_read([['email', '=', email]])
        if user:
            self.exist = True
            self.data = user[0]
            # TO-DO: map this field to active field of user so we can enable and disable andy account
            self._is_active = False
            self._is_authenticated = False
            self._is_anonymous = True
        # Random User id (it is like bacend session)
        self.user_id = "%s--%s" % (time.time(), random.random())
        UsersAuthenticator.user_sessions[self.user_id] = self

    @staticmethod
    def get_user_obj(user_id):
        return UsersAuthenticator.user_sessions.get(user_id, False)

    def validate_user(self, password):
        if check_password_hash(self.data.get('password_hash'), password):
            self._is_active = True
            self._is_authenticated = True
            self._is_anonymous = False

    def o_auth_validate(self):
        if self.oauth_data.get('email'):
            self._is_active = True
            self._is_authenticated = True
            self._is_anonymous = False

    def oauth_create_user(self):
        user_table = table_registry.users
        if self.oauth_data.get('email'):
            if not user_table.search([['email', '=', self.oauth_data.get('email')]]):
                user_table.create({
                    'name': self.oauth_data.get('name'),
                    'email': self.oauth_data.get('email')
                })

    def get_google_user_info(self, access_token):
        if access_token is None:
            return False

        from urllib2 import Request, urlopen, URLError

        headers = {'Authorization': 'OAuth '+access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                      None, headers)
        try:
            res = urlopen(req)
        except URLError:
            return False

        return json.loads(res.read())

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @is_active.deleter
    def is_active(self):
        del self._is_active

    # is_authenticated
    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

    @is_authenticated.deleter
    def is_authenticated(self):
        del self._is_authenticated

    # is_anonymous
    @property
    def is_anonymous(self):
        return self._is_anonymous

    @is_anonymous.setter
    def is_anonymous(self, value):
        self._is_anonymous = value

    @is_anonymous.deleter
    def is_anonymous(self):
        del self._is_anonymous

    def get_id(self):
        return self.user_id

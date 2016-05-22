from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Required, Email, EqualTo, ValidationError
from flask.ext.login import login_required, current_user
from werkzeug.security import check_password_hash

from orm.orm import TableRegistry

table_registry = TableRegistry()


class LoginForm(Form):
    email = StringField('User Name', validators=[Required()])
    password = StringField('password', validators=[Required()])


class SignUpForm(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email Id', validators=[Required(), Email(message='Please Valid Email Address')])
    password = PasswordField('password', validators=[Required()])
    password_cmp = PasswordField('password_cmp', validators=[Required(), EqualTo('password', message='Passwords must match.')])
    terms = BooleanField('accept terms')

    def validate_password(form, field):
        if len(field.data) < 8:
            raise ValidationError('Password must be 8 character long ')
        if not any([c.isdigit() for c in field.data]):
            raise ValidationError('Password must contain atleast one number')
        if all([c.isdigit() for c in field.data]):
            raise ValidationError('Password must contain atleast one alphabetic character')

    def validate_email(form, field):
        user = table_registry.users.search_read([['email', '=', field.data]])
        if user:
            raise ValidationError('User already exist for with this email')


class ChangepasswordForm(Form):
    current_password = PasswordField('current_password', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    password_cmp = PasswordField('password_cmp', validators=[Required(), EqualTo('password', message='Passwords must match.')])

    def validate_password(form, field):
        if len(field.data) < 8:
            raise ValidationError('Password must be 8 character long ')
        if not any([c.isdigit() for c in field.data]):
            raise ValidationError('Password must contain atleast one number')
        if all([c.isdigit() for c in field.data]):
            raise ValidationError('Password must contain atleast one alphabetic character')

    def validate_current_password(form, field):
        password_hash = current_user.data.get('password_hash')
        if not check_password_hash(password_hash, field.data):
            raise ValidationError('Wrong password')


class Edit_profile(Form):
    name = StringField('Name', validators=[Required()])
    email = StringField('Email Id', validators=[Required()])

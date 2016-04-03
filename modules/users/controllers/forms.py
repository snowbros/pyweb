from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Required, Email, EqualTo, ValidationError

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

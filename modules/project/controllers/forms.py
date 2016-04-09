from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Required, Email, EqualTo, ValidationError

from orm.orm import TableRegistry

table_registry = TableRegistry()


class ProjectForm(Form):
    email = StringField('User Name', validators=[Required()])
    password = StringField('password', validators=[Required()])


from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import Required


class ProjectForm(Form):
    name = StringField('Project Name', validators=[Required()])
    description = TextAreaField('Description', validators=[Required()])
    color = StringField('Dolor', validators=[Required()])
    date = StringField('Date', validators=[Required()])

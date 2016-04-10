from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import Required


class TaskForm(Form):
    name = StringField('Task Name', validators=[Required()])
    description = TextAreaField('Description', validators=[Required()])
    color = StringField('Dolor', validators=[Required()])
    date = StringField('Date', validators=[Required()])
    user_id = IntegerField('user_id')
    date_deadline = StringField('Date Deadline', validators=[Required()])
    state = StringField('Status', validators=[Required()])

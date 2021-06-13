from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Length


class SubmissionForm(FlaskForm):
	task = StringField("Task", validators=[Length(min=1, max=87)])
	urgent = BooleanField("Urgent")
	submit = SubmitField("Add task")
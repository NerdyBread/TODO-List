from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired


class SubmissionForm(FlaskForm):
	task = StringField("Task", validators=[Length(min=1, max=87)])
	urgent = BooleanField("Urgent")
	submit = SubmitField("Add task")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

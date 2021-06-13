from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user

from app import app
from app.forms import LoginForm, SubmissionForm
from app.models import User

task_list = []
urgent_task_list = []

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html", title="Home")


@app.route("/tasks")
def tasks():
	return render_template("tasks.html", title="Tasks", tasks=task_list, urgent_tasks=urgent_task_list)

@app.route("/add", methods=["GET", "POST"])
def add():
	form = SubmissionForm()
	if form.validate_on_submit():
		task = form.task.data
		if form.urgent.data:
			urgent_task_list.append(task)
		else:
			task_list.append(task)
		return redirect(url_for('tasks'))
	return render_template("add.html", title="Add task", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

# For the task delete buttons
@app.route("/delete/<index>")
def delete(index):
	task_list.pop(int(index)-1)
	return redirect(url_for('tasks'))

@app.route("/delete/urgent/<index>")
def delete_urgent(index):
	urgent_task_list.pop(int(index)-1)
	return redirect(url_for('tasks'))

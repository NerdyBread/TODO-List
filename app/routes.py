from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_migrate import current
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, SubmissionForm, SignUpForm
from app.models import User, Task

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html", title="Home")


@app.route("/tasks")
@login_required
def tasks():
	tasks = current_user.tasks
	task_list = [task.task for task in tasks if not task.urgent]
	urgent_list = [task.task for task in tasks if task.urgent]
	return render_template("tasks.html", title="Tasks", tasks=task_list, urgent_tasks=urgent_list)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
	form = SubmissionForm()
	if form.validate_on_submit():
		task = form.task.data
		urgent = form.urgent.data
		new_task = Task(task=task, urgent=urgent, author=current_user)
		db.session.add(new_task)
		db.session.commit()
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
		flash(f'Signed in as {current_user.username}')
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for signing up')
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Sign Up', form=form)

# For the task delete buttons
@app.route("/delete/<index>")
def delete(index):
	count = 0
	tasks = current_user.tasks
	print(tasks)
	for task in tasks:
		if not task.urgent:
			count += 1
		if count == int(index):
			print(task)
			db.session.delete(task)
			db.session.commit()
	return redirect(url_for('tasks'))

@app.route("/delete/urgent/<index>")
def delete_urgent(index):
	count = 0
	tasks = current_user.tasks
	for task in tasks:
		if task.urgent:
			count += 1
		if count == int(index):
			db.session.delete(task)
			db.session.commit()
	return redirect(url_for('tasks'))

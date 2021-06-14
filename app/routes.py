from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, SubmissionForm, SignUpForm
from app.models import User

task_list = []
urgent_task_list = []

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html", title="Home")


@app.route("/tasks")
@login_required
def tasks():
	return render_template("tasks.html", title="Tasks", tasks=task_list, urgent_tasks=urgent_task_list)

@app.route("/add", methods=["GET", "POST"])
@login_required
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
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

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
	task_list.pop(int(index)-1)
	return redirect(url_for('tasks'))

@app.route("/delete/urgent/<index>")
def delete_urgent(index):
	urgent_task_list.pop(int(index)-1)
	return redirect(url_for('tasks'))

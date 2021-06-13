import re
from flask import render_template, redirect, url_for, flash

from app import app
from app.forms import SubmissionForm

task_list = []
urgent_task_list = []

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

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
	return render_template("add.html", form=form)

@app.route("/tasks")
def tasks():
	return render_template("tasks.html", tasks=task_list, urgent_tasks=urgent_task_list)

@app.route("/delete/<index>")
def delete(index):
	task_list.pop(int(index)-1)
	return redirect(url_for('tasks'))

@app.route("/delete/urgent/<index>")
def delete_urgent(index):
	urgent_task_list.pop(int(index)-1)
	return redirect(url_for('tasks'))
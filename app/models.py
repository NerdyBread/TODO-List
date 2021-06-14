from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='author', lazy=True)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f'<User {self.username}>'

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(140))
	urgent = db.Column(db.Boolean)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Task {self.task}, urgent={self.urgent}, User {self.user_id}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
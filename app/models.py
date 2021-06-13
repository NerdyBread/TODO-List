from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='author', lazy=True)

	def __repr__(self):
		return f'<User {self.username}>'

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(140))
	urgent = db.Column(db.Boolean)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Task {self.task}, urgent={self.urgent}, User {self.user_id}>'
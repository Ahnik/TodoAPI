from flask_login import UserMixin
from app import db

# The table schema for storing the user data
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    # The fields of the table 'users'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Tasks', backref='users')
    
    def __repr__(self):
        return f'<Name: {self.name}>'
    
    def get_uid(self):
        return self.uid
    
# The table schema for storing the tasks
class Task(db.Model):
    __tablename__ = 'tasks'
    
    # The fields of the table 'tasks'
    task_id = db.Column(db.String(128), primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=False)
    
    def __repr__(self):
        return f'ID: {self.id}\nTitle: {self.title}\nDescription: {self.description}'
    
    def get_task_id(self):
        return self.task_id
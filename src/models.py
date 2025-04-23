from app import db
from werkzeug.security import check_password_hash

# The table schema for storing the user data
class User(db.Model):
    __tablename__ = 'user'
    
    # The fields of the table 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='user')
    
    def __repr__(self):
        return f'<Name: {self.name}>'
    
    def get_uid(self):
        return self.user_id
    
    def check_password(self, password):
       return check_password_hash(self.password, password)
    
# The table schema for storing the tasks
class Task(db.Model):
    __tablename__ = 'task'
    
    # The fields of the table 'task'
    task_id = db.Column(db.String(128), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user_task_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(7), nullable=False)
    
    def __repr__(self):
        return f'ID: {self.id}\nTitle: {self.title}\nDescription: {self.description}'
    
    def get_task_id(self):
        return self.task_id
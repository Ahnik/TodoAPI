from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Setting up the database
db = SQLAlchemy()

# Creating the function to create our Flask app
def create_app():
    '''This function creates the Flask application and returns it as a Python object'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    
    db.init_app(app)
    
    migrate = Migrate(app, db)
    return app
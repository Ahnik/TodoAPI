from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from secrets import token_hex

# Setting up the database
db = SQLAlchemy()

# Creating the function to create our Flask app
def create_app():
    '''This function creates the Flask application and returns it as a Python object'''
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = token_hex()
    
    # Setup the Flask-JWT-Extended extension
    app.config['JWT_SECRET_KEY'] = token_hex()
    jwt = JWTManager(app)
    
    db.init_app(app)
    
    # Setup the login manager for the app
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    from models import User
    
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return jsonify({'message':'Unauthorized'}), 401
    
    # We will be using a Bcrypt object to hash the user passwords
    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)
    
    migrate = Migrate(app, db)
    return app
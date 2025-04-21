from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Setting up the database
db = SQLAlchemy()

# Creating the function to create our Flask app
def create_app():
    '''This function creates the Flask application and returns it as a Python object'''
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'S*&f,,>A4h/3w2~5DMnUBr+{!~<$k{jT8Lj3~45]sGI<tcsf<96A]Ko,g1WxU/.'
    
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
        return redirect(url_for('index'))
    
    # We will be using a Bcrypt object to hash the user passwords
    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)
    
    migrate = Migrate(app, db)
    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import redis
from secrets import token_hex
from datetime import timedelta

# Setting up the database
db = SQLAlchemy()

# Set our redis connection for storing block-listed JWT tokens.
jwt_redis_blocklist = redis.StrictRedis(
    host='localhost', port=6379, db=0, decode_responses=True
)

# Time after which a JWT token expires.
ACCESS_EXPIRES = timedelta(hours=3)

# Creating the function to create our Flask app
def create_app():
    '''This function creates the Flask application and returns it as a Python object'''
    # Setup our Flask app
    app = Flask(__name__)
    
    # Setup connection to our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = token_hex()
    db.init_app(app)
    
    # Setup the Flask-JWT-Extended extension
    app.config['JWT_SECRET_KEY'] = token_hex()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
    jwt = JWTManager(app)
    
    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token_in_redis = jwt_redis_blocklist.get('jti')
        return token_in_redis is not None
        
    # We will be using a Bcrypt object to hash the user passwords
    bcrypt = Bcrypt(app)
    
    from routes import register_routes
    register_routes(app, db, bcrypt)
    
    migrate = Migrate(app, db)
    return app
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from models import User

def register_routes(app, db, bcrypt):
    # Endpoint to sign up a user
    @app.route('/register', methods=['POST'])
    def register():
        name = request.json.get('name', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not User.query.filter_by(email=email).one_or_none() and not User.query.filter_by(name=name).one_or_none():     
            hashed_password = bcrypt.generate_password_hash(password)   
            db.session.add(User(email=email, name=name, password=hashed_password)) 
            db.session.commit()
            
            user = User.query.filter_by(email=email).one_or_none()
            token = create_access_token(identity=user.uid)
            return jsonify(token=token)
        else:
            return jsonify({'message':'Name or email already exists'}), 200
    
    # Endpoint to log in a user
    @app.route('/login', methods=['POST'])
    def login():
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        user = User.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return jsonify({'message':'Wrong email or password'}), 401
        
        token = create_access_token(identity=user.uid)
        return jsonify(token=token)
        
    # Endpoint to add a task to the Todo list
    @app.route('/todos', methods=['POST'])
    @jwt_required
    def add_task():
        pass
    
    # Endpoint to update an existing todo
    @app.route('/todos/<int:id>', methods=['PUT'])
    @jwt_required
    def update_tasks(id):
        pass
    
    # Endpoint to delete an existing todo
    @app.route('/todos/<int:id>', methods='DELETE')
    @jwt_required
    def delete_tasks(id):
        pass
    
    # Endpoint to get the list of tasks of a user
    @app.route('/todos', methods=['GET'])
    @jwt_required
    def list_tasks():
        pass
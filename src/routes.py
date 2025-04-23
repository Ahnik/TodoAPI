from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import User, Task
from sqlalchemy import desc

def register_routes(app, db, bcrypt):
    # Endpoint to sign up a user
    @app.route('/register', methods=['POST'], endpoint='register_user')
    def register():
        try:
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']
        except KeyError:
            return jsonify({'message':'Bad Request'}), 400
        
        errors = {}
        
        if not isinstance(name, str):
            errors['name'] = 'Name must be a string'
        elif len(name) == 0:
            errors['name'] = 'Name must not be empty'
        
        if not isinstance(email, str):
            errors['email'] = 'Email must be a string'
        elif len(email) == 0:
            errors['email'] = 'Email must not be empty'
        
        if not isinstance(password, str):
            errors['password'] = 'Password must be a string'
        elif len(password) == 0:
            errors['password'] = 'Password must not be empty'
            
        if errors:
            return jsonify({'errors':errors}), 400
        
        if not User.query.filter_by(email=email).one_or_none() and not User.query.filter_by(name=name).one_or_none():     
            hashed_password = bcrypt.generate_password_hash(password)   
            db.session.add(User(email=email, name=name, password=hashed_password)) 
            db.session.commit()
            
            user = User.query.filter_by(email=email).one_or_none()
            token = create_access_token(identity=user.user_id)
            return jsonify(token=token), 201
        else:
            return jsonify({'message':'Name or email already exists'}), 200
    
    # Endpoint to log in a user
    @app.route('/login', methods=['POST'], endpoint='login_user')
    def login():
        try:
            email = request.json['email']
            password = request.json['password']
        except KeyError:
            return jsonify({'message':'Bad Request'}), 400
        
        errors = {}
        
        if not isinstance(email, str):
            errors['email'] = 'Email must be a string'
        elif len(email) == 0:
            errors['email'] = 'Email must not be empty'
        
        if not isinstance(password, str):
            errors['password'] = 'Password must be a string'
        elif len(password) == 0:
            errors['password'] = 'Password must not be empty'
            
        if errors:
            return jsonify({'errors':errors}), 400
        
        user = User.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return jsonify({'message':'Wrong email or password'}), 401
        
        token = create_access_token(identity=user.user_id)
        return jsonify(token=token), 200
        
    # Endpoint to add a task to the Todo list or list them
    @app.route('/todos', methods=['POST', 'GET'], endpoint='add_list_tasks')
    @jwt_required
    def add_list_tasks():
        user_id = get_jwt_identity()
        # If the request is a 'POST' request, the user can add a new task 
        if request.method == 'POST':
            try:
                title = request.json['title']
                description = request.json['description']
            except KeyError:
                return jsonify({'message':'Bad Request'}), 400
            
            errors = {}
            
            if not isinstance(title, str):
                errors['title'] = 'Title must be a string'
            elif len(title) == 0:
                errors['title'] = 'Title must not be empty'
            
            if not isinstance(description, str):
                errors['description'] = 'Description must be a string'
            elif len(description) == 0:
                errors['description'] = 'Description must not be empty'
                
            if errors:
                return jsonify({'errors':errors}), 400
            
            task = Task.query.filter_by(is_active=False, user_id=user_id).order_by(Task.user_task_id).first()
            if task:
                task.is_active = True
                task.title = title
                task.description = description
                user_task_id = task.user_task_id
                db.session.commit()
            else:
                last_task = Task.query.filter_by(user_id=user_id).order_by(desc(Task.user_task_id)).first()
                user_task_id = last_task.user_task_id + 1
                db.session.add(Task(user_id=user_id, user_task_id=user_task_id, title=title, description=description))
                db.session.commit()
            return jsonify({'message':'Task {user_task_id} successfully added'}), 201
        # If the request is a 'GET' request, the API will return a JSON array as the list of all the tasks of the user
        elif request.method == 'GET':
            tasks = Task.query.filter_by(user_id=user_id).all()
            json_array = []
            for task in tasks:
                json_object = {}
                json_object['id'] = task.user_task_id
                json_object['title'] = task.title
                json_object['description'] = task.description
                json_array.append(json_object)
            return jsonify(json_array), 200
    
    # Endpoint to update or delete an existing todo
    @app.route('/todos/<int:id>', methods=['PUT', 'DELETE'], endpoint='update_delete_task')
    @jwt_required
    def update_delete_tasks(id):
        user_id = get_jwt_identity()
        # If the request is a 'PUT' request, the user can update their tasks
        if request.method =='PUT':
            task = Task.query.filter_by(user_id=user_id, user_task_id=id).one_or_404()
            data = request.get_json()
            error = {}
            
            # We will first check whether the JSON payload is in the correct format
            if not isinstance(data, dict):
                return jsonify({'message':'Invalid JSON payload'}), 400
            
            if 'title' in data.keys():
                if not isinstance(data['title'], str):
                    error['title'] = 'Title must be a string'
                elif len(data['title']) == 0:
                    error['title'] = 'Title must not be empty'

            if 'description' in data.keys():
                if not isinstance(data['description'], str):
                    error['description'] = 'Description must be a string'
                elif len(data['description']) == 0:
                    error['description'] = 'Description must not be empty'
                    
            if error:
                return jsonify({'errors':error}), 400
            
            # Now, we will update the task requested
            if 'title' in data.keys():
                task.title = data['title'].strip()
            if 'description' in data.keys():
                task.description = data['description'].strip()
                
            db.session.commit()
            return jsonify({'message':f'Task {id} successfully updated'}), 200
        # If the request is a 'DELETE' request, then the user is asking to delete a task
        elif request.method == 'DELETE':
            task = Task.query.filter_by(user_id=user_id, user_task_id=id).one_or_404()
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message':f'Task {id} successfully deleted'}), 204
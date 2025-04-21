from flask import jsonify, request
from flask_login import login_user, logout_user, login_required
from models import User

def register_routes(app, db, bcrypt):
    # Endpoint to sign up a user
    @app.route('/register', methods=['POST'])
    def register():
        pass
    
    # Endpoint to log in a user
    @app.route('/login', methods=['POST'])
    def login():
        pass
    
    # Endpoint to add a task to the Todo list
    @app.route('/todos', methods=['POST'])
    @login_required
    def add_task():
        pass
    
    # Endpoint to update an existing todo
    @app.route('/todos/<int:id>', methods=['PUT'])
    @login_required
    def update_tasks(id):
        pass
    
    # Endpoint to delete an existing todo
    @app.route('/todos/<int:id>', methods='DELETE')
    @login_required
    def delete_tasks(id):
        pass
    
    # Endpoint to get the list of tasks of a user
    @app.route('/todos', methods=['GET'])
    @login_required
    def list_tasks():
        pass
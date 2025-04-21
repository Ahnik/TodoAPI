from flask import request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from models import User

def register_routes(app, db, bcrypt):
    # The default endpoint to take the user to the 'index.html' page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Endpoint to sign up a user
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            pass
        
    # Endpoinnt for logging in a user
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            pass
        
    # Endpoint for logging out a user
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    # Endpoint for adding a new task onto the Todo list
    @app.route('/todos', methods=['POST'])
    @login_required
    def add_task():
        pass
    
    # Endpoint for updating a task on the Todo list
    @app.route('/todos/<int:id>', methods=['PUT'])
    @login_required
    def update_task():
        pass
    
    # Endpoint for deleting a task on the Todo list
    @app.route('/todos/<int:id>', methods=['DELETE'])
    @login_required
    def delete_task():
        pass
    
    # Endpoint for listing out all the tasks
    @app.route('/todos', methods=['GET'])
    @login_required
    def list_tasks():
        pass
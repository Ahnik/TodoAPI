from app import create_app, db

flask_app = create_app()

if __name__ == '__main__':
    # Create the database if it doesn't exist
    with flask_app.app_context:
        db.create_all()
        
    flask_app.run(debug=True)
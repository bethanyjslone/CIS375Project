# add_user.py
from werkzeug.security import generate_password_hash
from PillLibraryApp import app, db  # make sure to import your actual Flask app and database
from PillLibraryApp.models import User

def add_user(username, password):
    # Push an application context so we can access the DB and app config
    with app.app_context():
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            # User doesn't exist, so we can add them
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)

            # Add the new user to the DB
            db.session.add(new_user)
            db.session.commit()
            print(f'User {username} added successfully.')
        else:
            print(f'User {username} already exists.')

if __name__ == '__main__':
    # Prompt for username and password
    username = input("Enter the new username: ")
    password = input("Enter the new password: ")

    # Call the function to add user
    add_user(username, password)
# run.py
from PillLibraryApp import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # You can perform additional setup tasks here if needed.

    app.run(debug=True)
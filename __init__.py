# PillLibraryApp/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = '_5#y2L"F4Q8z6nx1ec]/'
    db.init_app(app)

    # Register blueprints or route functions here if any
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    return app
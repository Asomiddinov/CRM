from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from os import path
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app.config.update(UPLOAD_PATH=os.path.join(dir_path, "static"))
    app.config["SECRET_KEY"] = 'bluiylvkjg udyitfiuyfghjg'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.app_context().push()
    db.init_app(app)
    migrate = Migrate(app, db)
    create_database(app)
    return app


def create_database(app):
    if not path.exists("instance/clients.sqlite3"):
        db.create_all(app=app)
        print("DB created!")

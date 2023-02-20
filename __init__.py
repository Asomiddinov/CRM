from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)
db = SQLAlchemy()

dir_path = os.path.dirname(os.path.realpath(__file__))
app.config.update(UPLOAD_PATH=os.path.join(dir_path, "static"))
app.config["SECRET_KEY"] = 'bluiylvkjg udyitfiuyfghjg'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)
migrate = Migrate(app, db)


def create_app():
    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.init_app(app)

    from forms import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app):
    if not path.exists("instance/clients.sqlite3"):
        with app.app_context():
            db.create_all(app=app)
            print("DB created!")

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from flask_migrate import Migrate

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
app.config.update(
    UPLOAD_PATH=os.path.join(dir_path, "static")
)
app.config["SECRET_KEY"] = 'bluiylvkjg udyitfiuyfghjg'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

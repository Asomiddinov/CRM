from application import routes
from flask import Flask
import os
app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
app.config.update(
    UPLOAD_PATH=os.path.join(dir_path, "static")
)
app.config["SECRET_KEY"] = 'bluiylvkjg udyitfiuyfghjg'

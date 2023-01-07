from application import routes
from flask import Flask
import os
app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
app.config.update(
    UPLOAD_PATH=os.path.join(dir_path, "static")
)
app.config["SECRET_KEY"] = '06fc086ccafd843a0213129a537a2b7b62c52bbe'

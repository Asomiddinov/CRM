from routes import app
from __init__ import db

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

from flask import Flask
from .database import db
from .routes import api
from flask_cors import CORS   # 👈 import CORS

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)   # 👈 enable CORS for all routes

    app.register_blueprint(api)

    return app

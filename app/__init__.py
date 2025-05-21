from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    from .routes.user_routes import user_bp
    from .routes.task_routes import task_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)

    return app

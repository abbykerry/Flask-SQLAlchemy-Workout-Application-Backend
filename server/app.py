from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import register_routes


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    Migrate(app, db)
    register_routes(app)

    return app


app = create_app()

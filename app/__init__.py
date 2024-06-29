from flask import Flask
from app.extensions import db, migrate
from app.main.views import main_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp, url_prefix='')

    return app



import os

import redis
from flask import Flask
from flask_session import Session

from App.model import db
from App.views import school, user

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def create_app():
    template_dir = os.path.join(BASE_DIR, 'templates')
    static_dir = os.path.join(BASE_DIR, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    app.register_blueprint(blueprint=school, url_prefix='/school')
    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/school'

    se = Session()
    db.init_app(app=app)
    se.init_app(app=app)
    return app
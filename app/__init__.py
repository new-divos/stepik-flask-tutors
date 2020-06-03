from flask import Flask

from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()


def create_app(config_cls):
    app = Flask(__name__)
    app.config.from_object(config_cls)
    config_cls.init_app(app)

    bootstrap.init_app(app)

    return app

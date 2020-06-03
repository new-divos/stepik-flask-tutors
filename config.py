import json
import os
from pathlib import Path

from flask import g


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', ":'(")
    APP_STORAGE_DIR = Path(os.getenv('APP_STORAGE_DIR', str(Path.cwd())))
    APP_STORAGE_FILE = os.getenv('APP_STORAGE_FILE', 'data.json')

    @classmethod
    def init_app(cls, app):
        data_path = cls.get_storage_path()
        if not data_path.exists() or not data_path.is_file():
            raise RuntimeError(f"Cannot load data from the file {data_path}")

        with open(data_path, encoding='utf-8') as f:
            data = json.load(f)

        with app.app_context():
            g.goals = data.get('goals')
            g.teaches = data.get('teaches')

    @classmethod
    def get_storage_path(cls):
        return cls.APP_STORAGE_DIR / cls.APP_STORAGE_FILE


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

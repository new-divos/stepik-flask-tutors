import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', ":'(")
    APP_STORAGE_DIR = Path(os.getenv('APP_STORAGE_DIR', str(Path.cwd())))
    APP_STORAGE_FILE = os.getenv('APP_STORAGE_FILE', 'data.json')

    @classmethod
    def init_app(cls, app):
        pass

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

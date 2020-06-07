import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', ":'(")
    APP_STORAGE_DIR = Path(os.getenv('APP_STORAGE_DIR', str(Path.cwd())))
    APP_STORAGE_FILE = os.getenv('APP_STORAGE_FILE', 'data.json')
    APP_STORAGE_LOCATION = os.getenv('APP_STORAGE_LOCATION', 'local')
    APP_STORAGE_S3_REGION = os.getenv('APP_STORAGE_S3_REGION', '')
    APP_STORAGE_S3_BUCKET = os.getenv('APP_STORAGE_S3_BUCKET', '')
    APP_STORAGE_S3_ACCESS_KEY_ID = os.getenv('APP_STORAGE_S3_ACCESS_KEY_ID', '')
    APP_STORAGE_S3_SECRET_KEY_ID = os.getenv('APP_STORAGE_S3_SECRET_KEY_ID', '')

    @classmethod
    def init_app(cls, app):
        app.config['APP_STORAGE_PATH'] = cls.get_storage_path()

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

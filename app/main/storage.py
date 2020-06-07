from collections import OrderedDict
import json

import boto3
from flask import current_app


class Storage:
    __weekdays = OrderedDict([
                ("mon", "Понедельник"),
                ("tue", "Вторник"),
                ("wed", "Среда"),
                ("thu", "Четверг"),
                ("fri", "Пятница"),
                ("sat", "Суббота"),
                ("sun", "Воскресение"),
    ])

    __opportunities = [
        ("op1", "1-2 часа в неделю"),
        ("op2", "3-5 часов в неделю"),
        ("op3", "5-7 часов в неделю"),
        ("op4", "7-10 часов в неделю"),
    ]

    def __new__(cls):
        if not hasattr(cls, '_Storage__instance'):
            cls.__instance = super(Storage, cls).__new__(cls)

        if not hasattr(cls, '_Storage__cache'):
            cls.__cache = {'goals': [], 'teachers': []}

        if not cls.__cache.get('goals') or not cls.__cache.get('teachers'):
            cls.load()

        return cls.__instance

    @classmethod
    def load(cls):
        if current_app.config['APP_STORAGE_LOCATION'] == 'local':
            try:
                with open(current_app.config['APP_STORAGE_PATH'], encoding='utf-8') as f:
                    cls.__cache = json.load(f)

            except OSError:
                cls.__cache = {'goals': [], 'teachers': []}

        elif current_app.config['APP_STORAGE_LOCATION'] == 's3':
            s3 = boto3.resource('s3',
                                region_name=current_app.config['APP_STORAGE_S3_REGION'],
                                aws_access_key_id=current_app.config['APP_STORAGE_S3_ACCESS_KEY_ID'],
                                aws_secret_access_key=current_app.config['APP_STORAGE_S3_SECRET_KEY_ID'])

            data = s3.Object(current_app.config['APP_STORAGE_S3_BUCKET'],
                             current_app.config['APP_STORAGE_FILE']).get()['Body'].read().decode('utf-8')
            cls.__cache = json.loads(data)

    @property
    def goals(self):
        return self.__cache.get('goals', [])

    @property
    def teachers(self):
        return self.__cache.get('teachers', [])

    @property
    def weekdays(self):
        return self.__weekdays

    @property
    def opportunities(self):
        return self.__opportunities

    def update(self):
        if current_app.config['APP_STORAGE_LOCATION'] == 'local':
            with open(current_app.config['APP_STORAGE_PATH'], 'w', encoding='utf-8') as f:
                json.dump(self.__cache, f, indent=4, ensure_ascii=False)

        elif current_app.config['APP_STORAGE_LOCATION'] == 's3':
            s3 = boto3.resource('s3',
                                region_name=current_app.config['APP_STORAGE_S3_REGION'],
                                aws_access_key_id=current_app.config['APP_STORAGE_S3_ACCESS_KEY_ID'],
                                aws_secret_access_key=current_app.config['APP_STORAGE_S3_SECRET_KEY_ID'])

            s3.Object(current_app.config['APP_STORAGE_S3_BUCKET'],
                      current_app.config['APP_STORAGE_FILE']).put(Body=json.dumps(self.__cache,
                                                                                  indent=4,
                                                                                  ensure_ascii=False))

from collections import OrderedDict
import json

from flask import current_app


class Storage:
    def __new__(cls):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(Storage, cls).__new__(cls)

        if not hasattr(cls, '__days_of_week'):
            cls.__weekdays = OrderedDict([
                ("mon", "Понедельник"),
                ("tue", "Вторник"),
                ("wed", "Среда"),
                ("thu", "Четверг"),
                ("fri", "Пятница"),
                ("sat", "Суббота"),
                ("sun", "Воскресение"),
            ])

        if not hasattr(cls, '__cache'):
            cls.__cache = {'goals': [], 'teachers': []}

        if not cls.__cache.get('goals') or not cls.__cache.get('teachers'):
            try:
                with open(current_app.config['APP_STORAGE_PATH'], encoding='utf-8') as f:
                    cls.__cache = json.load(f)

            except OSError:
                cls.__cache = {'goals': [], 'teachers': []}

        return cls.__instance

    @property
    def goals(self):
        return self.__cache.get('goals', [])

    @property
    def teachers(self):
        return self.__cache.get('teachers', [])

    @property
    def weekdays(self):
        return self.__weekdays

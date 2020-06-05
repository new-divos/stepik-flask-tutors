from collections import OrderedDict
import json

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
        try:
            with open(current_app.config['APP_STORAGE_PATH'], encoding='utf-8') as f:
                cls.__cache = json.load(f)

        except OSError:
            cls.__cache = {'goals': [], 'teachers': []}

    @property
    def goals(self):
        return self.__cache.get('goals', [])

    @property
    def teachers(self):
        return self.__cache.get('teachers', [])

    @property
    def weekdays(self):
        return self.__weekdays

    def update(self):
        with open(current_app.config['APP_STORAGE_PATH'], 'w', encoding='utf-8') as f:
            json.dump(self.__cache, f, indent=4, ensure_ascii=False)

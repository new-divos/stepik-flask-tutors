from flask import render_template

from . import main


# noinspection PyUnusedLocal
@main.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',
                           message="404. Страница не найдена"), 404


# noinspection PyUnusedLocal
@main.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html',
                           message="500. Внутренняя ошибка сервера"), 500

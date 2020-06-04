from collections import OrderedDict

from flask import abort, render_template

from . import main
from .storage import Storage


@main.route('/')
def index():
    return 'Hello from tutors!'


@main.route('/goals/<code>/')
def render_goal(code: str):
    pass


@main.route('/profiles/<int:id>/')
def render_profile(id: int):
    storage = Storage()
    teacher = next((t for t in storage.teachers if t['id'] == id), None)
    if teacher is None:
        abort(404)

    goals = [g['title'] for g in storage.goals if g['code'] in teacher['goals']]

    time_table = OrderedDict()
    for code, name in storage.days_of_week.items():
        hour_lst = [('0' + hour if len(hour) < 5 else hour, int(hour.split(':')[0]))
                    for hour, free in teacher['free'].get(code, dict()).items() if free]
        hour_lst.sort(key=lambda item: item[1])

        time_table[(code, name)] = OrderedDict(hour_lst)

    return render_template('profile.html',
                           teacher=teacher,
                           goals=goals,
                           time_table=time_table)


@main.route('/booking/<int:id>/<code>/<int:hour>/')
def render_booking(id, code, hour):
    return 'It works!'

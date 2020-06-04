from collections import OrderedDict
from random import sample

from flask import abort, render_template

from . import main
from .storage import Storage
from .forms import BookingForm


@main.route('/')
def index():
    storage = Storage()
    teachers = sample(storage.teachers, k=6)
    teachers.sort(key=lambda item: item['rating'], reverse=True)

    return render_template('index.html', goals=storage.goals, teachers=teachers)


@main.route('/goals/<code>/')
def render_goal(code: str):
    storage = Storage()
    goal = next((g['title'] for g in storage.goals if g['code'] == code), '').lower()
    teachers = [t for t in storage.teachers if code in t['goals']]
    teachers.sort(key=lambda item: item['rating'], reverse=True)

    return render_template('goal.html', goal=goal, teachers=teachers)


@main.route('/profiles/<int:id>/')
def render_profile(id: int):
    storage = Storage()
    teacher = next((t for t in storage.teachers if t['id'] == id), None)
    if teacher is None:
        abort(404)

    goals = [g['title'] for g in storage.goals if g['code'] in teacher['goals']]

    time_table = OrderedDict()
    for code, name in storage.weekdays.items():
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
    storage = Storage()
    teacher = next((t for t in storage.teachers if t['id'] == id), None)
    if teacher is None:
        abort(404)

    if code not in storage.weekdays:
        abort(404)

    time = f'{hour}:00'
    if time in teacher['free'].get(code, dict()):
        if not teacher['free'][code].get(time, False):
            abort(404)
    else:
        abort(404)

    form = BookingForm()
    return render_template('booking.html',
                           teacher=teacher,
                           weekday=(code, storage.weekdays[code]),
                           time=time,
                           form=form)


@main.route('/booking_done/')
def render_booking_done():
    return 'It works!'


@main.route('/request/')
def render_request():
    return 'It works!'


@main.route('/request_done/')
def render_request_done():
    return 'It works!'

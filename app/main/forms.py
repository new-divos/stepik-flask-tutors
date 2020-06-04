from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired


class BookingForm(FlaskForm):
    client_weekday = HiddenField(id='clientWeekday')
    client_time = HiddenField(id='clientTime')
    client_teacher = HiddenField(id='clientTeacher')

    client_name = StringField("Вас зовут",
                              id='clientName',
                              validators=[InputRequired()])
    client_phone = StringField("Ваш телефон",
                               id='clientPhone',
                               validators=[InputRequired()])

    submit = SubmitField("Записаться на пробный урок")

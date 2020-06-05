from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Regexp


class BookingForm(FlaskForm):
    PHONE_NUMBER_REGEXP = r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'

    client_weekday = HiddenField(id='clientWeekday')
    client_time = HiddenField(id='clientTime')
    client_teacher = HiddenField(id='clientTeacher')

    client_name = StringField("Вас зовут",
                              id='clientName',
                              validators=[DataRequired("Должно быть задано имя клиента")])
    client_phone = StringField("Ваш телефон",
                               id='clientPhone',
                               validators=[DataRequired("Должен быть задан номер телефона клиента"),
                                           Regexp(PHONE_NUMBER_REGEXP,
                                                  message="Номер телефона должен соответствовать шаблону")])

    submit = SubmitField("Записаться на пробный урок")

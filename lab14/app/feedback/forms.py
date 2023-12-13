from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired, Length

class CreateFeedbackForm(FlaskForm):
    name = StringField("Імʼя", validators=[DataRequired("Це поле обовʼязкове"), Length(min=1, max=100)])
    email = EmailField("Пошта", validators=[DataRequired("Це поле обовʼязкове"), Length(min=1, max=100)])
    description = StringField("Опишіть, що ви думаєте", validators=[DataRequired("Це поле обовʼязкове"), Length(min=1, max=300)])
    rate = SelectField("Оцінка", choices=[
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    ])
    submit = SubmitField("Надіслати")
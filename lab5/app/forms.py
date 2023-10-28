from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Імʼя", validators=[DataRequired("Це поле обовʼязкове")])
    password = PasswordField("Пароль", validators=[
                            DataRequired("Це поле обовʼязкове"),
                            Length(min=4, max=10)
                        ])
    remember = BooleanField("Запамʼятати")
    submit = SubmitField("Увійти")
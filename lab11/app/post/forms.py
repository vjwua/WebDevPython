from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Length, InputRequired

class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[InputRequired(), Length(min=2, max=100)])
    text = TextAreaField('Текст', validators=[Length(max=500)])
    picture = FileField('Зображення', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Тип', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    submit = SubmitField('Створити')
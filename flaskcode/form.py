from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField ,EmailField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')

class flaker(FlaskForm):
    name=StringField("Name",validators=[DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('submit')
    
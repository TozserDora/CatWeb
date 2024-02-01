from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from flask_ckeditor import CKEditorField


class SignUpForm(FlaskForm):
    user = StringField("Username", validators=[DataRequired(message="Please enter your username")])
    email = EmailField("Email", validators=[DataRequired(message="Please enter your email")])
    password = PasswordField("Password", validators=[DataRequired(message="Please enter your password")])
    password_2 = PasswordField("Password again", validators=[DataRequired(message="Please repeat your password")])
    submit = SubmitField("Sign up")


class LogInForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="Please enter your email")])
    password = PasswordField("Password", validators=[DataRequired(message="Please enter your password")])
    submit = SubmitField("Log in")


class UploadForm(FlaskForm):
    title = StringField("Title")
    description = CKEditorField("Tell us about your picture")
    photo = FileField("Find a cute photo for us", validators=[FileRequired()])
    submit = SubmitField("Upload")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from flask_wtf.file import FileField, FileRequired
from flask_ckeditor import CKEditorField


class SignUpForm(FlaskForm):
    user = StringField("Username")
    email = EmailField("Email")
    password = PasswordField("Password")
    password_2 = PasswordField("Please, repeat your password!")
    submit = SubmitField("Sign up")


class LogInForm(FlaskForm):
    email = EmailField("Email")
    password = PasswordField("Password")
    submit = SubmitField("Log in")


class UploadForm(FlaskForm):
    title = StringField("Title")
    description = CKEditorField("Tell us about your picture")
    photo = FileField("Find a cute photo for us", validators=[FileRequired()])
    submit = SubmitField("Upload")
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, length, equal_to
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed

class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8, max=64, message="Password must be between 8 and 64 characters long")])
    r_pass = PasswordField('Repeat Password', validators=[DataRequired(), equal_to('password', message='Passwords do not match')])
    uname = StringField('Username', validators=[DataRequired(), length(min=5)])
    check = BooleanField('Keep Me Signed Me', default=False)
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    s_title = StringField('Subtitle', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    background_img = FileField('Background image', validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')
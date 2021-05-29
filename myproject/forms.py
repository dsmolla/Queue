from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, 
                        BooleanField, TextAreaField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from myproject.models import User

from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email(), Length(max=32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('First name is required.'),
                                                  Length(min=2, max=32, message='First Name should be 2-32 chars.')])
    lname = StringField('Last Name', validators=[DataRequired('Last name is required.'),
                                                 Length(min=2, max=32, message='Last Name should be 2-32 chars.')])
    email = StringField('Email', validators=[DataRequired('Email is required.'),
                                             Email('Please provide a valid email address.'),
                                             Length(max=32, message='Email should be less than 32 chars.')])

    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=32, message='Password should be 8-32 chars.'),
                                                     EqualTo('pass_conf', message=' Passwords must match.')])
    pass_conf = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def email_exists(self):
        if User.query.filter_by(email=self.email.data).first():
            return True


class AskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    question = TextAreaField(validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Post Question')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Type your answer here.', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Post Answer')
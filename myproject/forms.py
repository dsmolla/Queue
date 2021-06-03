from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                        BooleanField, TextAreaField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from myproject.models import User
from werkzeug.security import check_password_hash
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email(), Length(max=32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

    def password_validate(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None and check_password_hash(user.password, self.password.data):
            return True
        return False


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

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            return True


class ChangePassword(FlaskForm):
    cur_password = PasswordField('Current Password', validators=[DataRequired(),
                                                     Length(min=8, max=32, message='Password should be 8-32 chars.')])
    new_password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=32, message='Password should be 8-32 chars.'),
                                                     EqualTo('pass_conf', message=' Passwords must match.')])
    pass_conf = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Change Password')



class AskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    question = TextAreaField(validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post Question')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Type your answer here.', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Post Answer')


class EditForm(FlaskForm):
    title = StringField(validators=[DataRequired(), Length(max=200)])
    question = TextAreaField(validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email(), Length(max=32)])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is None:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=32, message='Password should be 8-32 chars.'),
                                                     EqualTo('pass_conf', message=' Passwords must match.')])
    pass_conf = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
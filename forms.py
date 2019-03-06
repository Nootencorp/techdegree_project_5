from flask_wtf import Form
from wtforms import (StringField, PasswordField, TextAreaField,
                     DateField, IntegerField)
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)
from models import Entry, User


def title_exists(form, field):
    if Entry.select().where(Entry.title == field.data).exists():
        raise ValidationError('Entry with that title already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class AddEntry(Form):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            title_exists
        ]
    )
    date = DateField(
        'Date (MM/DD/YYYY)',
        format='%m/%d/%Y',
        validators=[
            DataRequired()
        ]
    )
    time_spent = IntegerField(
        'Time Spent (in minutes)',
        validators=[
            DataRequired()
        ]
    )
    learned = TextAreaField(
        'What I Learned',
        validators=[
            DataRequired()
        ]
    )
    resources = TextAreaField(
        'Resources to Remember',
        validators=[
            DataRequired()
        ]
    )
    tags = StringField(
        'Tags (separate with a space)',
    )


class EditEntry(Form):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
        ]
    )
    date = DateField(
        'Date (MM/DD/YYYY)',
        format='%m/%d/%Y',
        validators=[
            DataRequired()
        ]
    )
    time_spent = IntegerField(
        'Time Spent (in minutes)',
        validators=[
            DataRequired()
        ]
    )
    learned = TextAreaField(
        'What I Learned',
        validators=[
            DataRequired()
        ]
    )
    resources = TextAreaField(
        'Resources to Remember (resource name, space, url)',
        validators=[
            DataRequired()
        ]
    )
    tags = StringField(
        'Tags (separate with a space)',
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

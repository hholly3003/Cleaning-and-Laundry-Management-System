from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)

class RegisterForm(FlaskForm):
    """ User Registration Form """
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Enter a valid email"),
            Length(min=4)
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            EqualTo("password",
                message="Password entered do not match")
        ]
    )
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    """ User Login Form """
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Enter a valid email")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()])
    submit = SubmitField("Login")

class ProfileForm(FlaskForm):
    """ Create Profile Form """
    username = StringField("username")
    firstname = StringField(
        "First name",
        validators=[
            DataRequired(),
            Length(min=1)   
        ]
    )
    lastname = StringField(
        "Last name",
        validators=[
            DataRequired(),
            Length(min=1)   
        ]
    )
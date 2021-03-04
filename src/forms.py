from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FormField, IntegerField, DateField, TimeField, SelectField, TextAreaField
from wtforms.fields.html5 import TelField
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

# class TelephoneForm(FlaskForm):
#     country_code = StringField(
#         "Country Code",
#         validators=[DataRequired()]   
#     )
#     area_code = StringField(
#         "Area Code",
#         validators=[DataRequired()]
#     )
#     number = StringField("Number")

class AddressForm(FlaskForm):
    street_name = StringField(
        "Street Name",
        validators=[
            DataRequired(),
            Length(min=4)
        ]
    )
    suburb = StringField(
        "Suburb",
        validators=[
            DataRequired(),
            Length(min=4)
        ]
    )
    state = SelectField(
        "State",
        choices=[
            (1, "ACT"),
            (2, "NSW"),
            (3, "VIC"),
            (4, "QLD"),
            (5, "SA"),
            (6, "TAS"),
            (7, "WA")
        ],
        validators=[DataRequired()]
    )
    postcode = IntegerField(
        "Post Code",
        validators=[DataRequired()]
    )

class JobForm(FlaskForm):
    """Create Job Form"""
    cust_name = StringField(
        "Customer name",
        validators=[
            DataRequired(),
            Length(min=1,
                message="Customer name must be at least 1 character")
        ]
    )
    contact_num = TelField("Contact Number")
    job_requested = SelectField(
        "Job Requested",
        choices=[
            (1,"Cleaning"),
            (2,"Laundry")
        ],
        coerce=int,
        validators=[DataRequired()]
    )
    job_date = DateField(
        "Job Date",
        validators=[DataRequired(message="please select a date")]
    )
    job_time = TimeField(
        "Job Time",
        validators = [DataRequired(message="please specify the time")]
    )
    job_address = FormField(AddressForm)
    notes = TextAreaField("Notes")
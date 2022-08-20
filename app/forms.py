from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo

# name, phone, street_address, city, state, email
class PhonebookForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired()] + \
        [Length(min=7, max=14)])
    street_address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    email = StringField('Email')
    submit = SubmitField()
    # okay so I decided from the user's pov, I would be annoyed if I HAD to add
    # a full address and email when most people don't know that information
    # anymore these days, besides I think this site could have an 'edit contact'
    # option to add that info later


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()]) 
    # I don't like coming up with usernames, so everyone gets to login with their email (:
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()
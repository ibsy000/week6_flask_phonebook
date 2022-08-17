from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# name, phone, street_address, city, state, email
class PhonebookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    street_address = StringField('Address', validators=[DataRequired()] + [Length(min=7, max=14)])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField()
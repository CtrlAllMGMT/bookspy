from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from datetime import datetime

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    address = TextAreaField('Address')
    submit = SubmitField('Add Employee')

class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    address = TextAreaField('Address')
    submit = SubmitField('Add Customer')

class PartForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Part')

class CarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1900, max=datetime.now().year)])
    vin = StringField('VIN', validators=[DataRequired(), Length(min=17, max=17)])
    submit = SubmitField('Add Car')

class OrderForm(FlaskForm):
    customer_id = IntegerField('Customer', validators=[DataRequired()])
    car_id = IntegerField('Car', validators=[DataRequired()])
    submit = SubmitField('Create Order')
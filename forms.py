from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.fields import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from __init__ import db
from flask_login import UserMixin


class QRCodeData(FlaskForm):
    dat = StringField("Data", validators=[
        DataRequired(), Length(min=3, max=500)])
    submit = SubmitField("Generate QRCode")


class Mine(FlaskForm):
    client = StringField("Client", validators=[
                         DataRequired(), Length(min=3, max=500)])
    address = StringField("Address", validators=[
                          DataRequired(), Length(min=3, max=500)])
    quantity = StringField("Quantity", validators=[
                           DataRequired(), Length(max=500)])
    mark = StringField("Mark", validators=[
                       DataRequired(), Length(min=3, max=100)])
    price = IntegerField("Price", validators=[DataRequired()])
    currency = SelectField("Currency", choices=["UZS", "USD", "EUR", "RUB"])
    paid = IntegerField("Paid", validators=[DataRequired()])
    driver = StringField("Driver", validators=[
                         DataRequired(), Length(min=3, max=500)])
    date = DateField("Date", validators=[DataRequired()])
    approve = SelectField("Agreement", choices=[
                          "O'tkazib yuboring!", "O'tkazib yubormang!"])
    submit = SubmitField("Confirm")


# Data Base Class:
class Users(db.Model):
    id = db.Column("user_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(250))
    email = db.Column("email", db.String(250))
    address = db.Column("address", db.String(250))

    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

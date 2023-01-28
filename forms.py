from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.fields import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func


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


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# User Class:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(150))
    fullname = db.Column(db.String(250))
    comment = db.Column(db.String(250))
    notes = db.relationship("Note")

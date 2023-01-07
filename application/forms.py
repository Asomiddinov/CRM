from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.fields import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class QRCodeData(FlaskForm):
    dat = StringField("Data", validators=[
        DataRequired(), Length(min=3, max=500)])
    submit = SubmitField("Generate QRCode")


class Mine(FlaskForm):
    client = StringField("Client", validators=[
                         DataRequired(), Length(min=3, max=500)])
    quantity = StringField("Quantity", validators=[
                           DataRequired(), Length(min=3, max=500)])
    mark = StringField("Mark", validators=[
                       DataRequired(), Length(min=3, max=100)])
    price = IntegerField("Price", validators=[DataRequired()])
    paid = BooleanField("Is Paid?", validators=[DataRequired()])
    date = DateField("Date")
    submit = SubmitField("Confirm")

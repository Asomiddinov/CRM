from wtforms import StringField, SubmitField, IntegerField
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
    mark = StringField("Mark", DataRequired(), Length(min=3, max=100))
    paid = IntegerField("Paid", validators=[DataRequired()])
    date = DateField("Date", format="%d-%m-%Y")

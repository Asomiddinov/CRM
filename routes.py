from __init__ import app, db
from flask import render_template, request, flash, redirect, url_for
from forms import QRCodeData, Mine, Users
import secrets
import qrcode


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home Page")


@app.route("/info")
def layout():
    return render_template("info.html")


@app.route("/generator", methods=["GET", "POST"])
def generator():
    form = QRCodeData()
    if request.method == "POST":
        if form.validate_on_submit():
            dat = form.dat.data
            image_name = f"{secrets.token_hex(10)}.png"
            qrcode_location = f"{app.config['UPLOAD_PATH']}/{image_name}"
            try:
                my_qrcode = qrcode.make(
                    str(dat)).save(qrcode_location)
            except Exception as e:
                print(e)
            return render_template("generated.html", title="Generated 🔢", image=image_name)
    else:
        return render_template("generator.html", title="🔢", form=form)


@app.route("/mine", methods=["GET", "POST"])
def mine():
    form = Mine()
    client = form.client.data
    address = form.address.data
    quantity = form.quantity.data
    mark = form.mark.data
    price = form.price.data
    currency = form.currency.data
    paid = form.paid.data
    driver = form.driver.data
    date = form.date.data
    approve = form.approve.data
    return render_template("act.html", form=form, client=client, address=address, quantity=quantity, mark=mark, price=price, currency=currency, paid=paid, driver=driver, date=date, approve=approve)


@app.route("/acted", methods=["GET", "POST"])
def acted():
    form = Mine()
    return render_template("acted.html", form=form, client=form.client.data, address=form.address.data, qantity=form.quantity.data, mark=form.mark.data,
                           price=form.price.data, currency=form.currency.data, paid=form.paid.data, driver=form.driver.data, date=form.date.data,
                           approve=form.approve.data)


@app.route("/users")
def users():
    return render_template("users.html", users=Users.query.all())

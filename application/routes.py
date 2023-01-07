from application.__init__ import app
from flask import render_template, request, flash
from application.forms import QRCodeData, Mine
import secrets
import qrcode


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home Page 🔢")


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
            return render_template("generated.html", title="Generated", image=image_name)
    else:
        return render_template("generator.html", title="Index Page", form=form)


@app.route("/mine", methods=["GET", "POST"])
def mine():
    form = Mine()
    if request.method == "POST":
        if form.validate_on_submit():
            client = form.client.data
            quantity = form.quantity.data
            mark = form.mark.data
            paid = form.paid.data
            return render_template("act.html", form=form, client=client, quantity=quantity, mark=mark, paid=paid)
    else:
        flash("No post created for this code!", "error")
        return render_template("index.html")

from __init__ import create_app, db
from flask import render_template, request, flash, redirect, url_for
from forms import QRCodeData, Mine, User
import secrets
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
app = create_app()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home Page", user=current_user)


@app.route("/info")
def info():
    return render_template("info.html", user=current_user)


@app.route("/generator", methods=["GET", "POST"])
@login_required
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
            return render_template("generated.html", title="Generated 🔢", image=image_name, user=current_user)
    else:
        return render_template("generator.html", title="🔢", form=form, user=current_user)


@app.route("/mine", methods=["GET", "POST"])
@login_required
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
    return render_template("act.html", form=form, client=client, address=address, quantity=quantity, mark=mark, price=price, currency=currency, paid=paid, driver=driver, date=date, approve=approve,
                           user=current_user)


@app.route("/acted", methods=["GET", "POST"])
def acted():
    form = Mine()
    return render_template("acted.html", form=form, client=form.client.data, address=form.address.data, qantity=form.quantity.data, mark=form.mark.data,
                           price=form.price.data, currency=form.currency.data, paid=form.paid.data, driver=form.driver.data, date=form.date.data,
                           approve=form.approve.data,
                           user=current_user)


@app.route("/users")
def users():
    return render_template("users.html", user=current_user)


@app.route("/sign_up", methods=["GET", "POST"])
@login_required
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        fullname = request.form.get("fullname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        comment = str(password1)
        user = User.query.filter_by(email=email).first()
        if user.email == "basomiddinov@gmail.com":
            if user:
                flash("This email is already have. Use another!", category="error")
            elif len(email) < 5:
                flash("At least 6 characters for email, please!", category="error")
            elif password1 != password2:
                flash("Passwords don't match", category="error")
            elif len(password1) < 5:
                flash("At least 6 characters for password, please", category="error")
            else:
                new_user = User(email=email, fullname=fullname, comment=comment, password=generate_password_hash(
                    password1, method="sha256"))
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember=True)
                flash("Account created successfully!", category="success")
                return redirect(url_for("index"))
        else:
            flash("You're not admin!", category="error")
    return render_template("sign_up.html", user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("index"))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("This user doesn't exist", category="error")
    return render_template("login.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

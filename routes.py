from __init__ import create_app, db
from flask import render_template, request, flash, redirect, url_for
from forms import QRCodeData, Mine, User, Note, Reg
import secrets
import qrcode
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import select, func
import numpy as np
import pandas as pd
app = create_app()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="uzbaba systems 👨🏻‍💻", user=current_user)


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


@app.route("/action", methods=["GET", "POST"])
@login_required
def acted():
    form = Mine()
    reg = Reg(client=request.form.get("client"), address=request.form.get("address"), quantity=request.form.get("quantity"),
              paid=request.form.get("paid"), driver=request.form.get("driver"), date=request.form.get("date"), approve=request.form.get("approve"),
              mark=request.form.get("mark"), price=request.form.get('price'), currency=request.form.get("currency"),
              user_fullname=request.form.get("user_fullname"), client_id=request.form.get("client_id"))
    # reg = Reg.query.all()
    if request.method == "POST":
        if reg:
            db.session.add(reg)
            db.session.commit()
            flash("Registered to database!", "success")
            return redirect(url_for("info"))
    else:
        return render_template("action.html", user=current_user, form=form)


@app.route("/info", methods=["GET", "POST"])
def info():
    form = Mine()
    if form.validate_on_submit:
        reg = Reg.query.filter_by(id=Reg.id).all()
        balance, balance_paid, balance_price = 0, 0, 0
        for i in reg:
            balance = balance + i.paid - i.price
            balance_paid = balance_paid + i.paid
            balance_price = balance_price + i.price
        return render_template("info.html", form=form, reg=reg, user=current_user, balance=balance, balance_paid=balance_paid, balance_price=balance_price)


@app.route("/info/<client>/<client_id>")
def info_client(client, client_id):
    form = Mine()
    if client:
        e = Reg.query.filter_by(client=client, client_id=client_id).all()
        balance, balance_paid, balance_price = 0, 0, 0
        for i in e:
            balance = balance + i.paid - i.price
            balance_paid = balance_paid+i.paid
            balance_price = balance_price+i.price
        return render_template("info_client.html", user=current_user, e=e, form=form, balance=balance, balance_paid=balance_paid, balance_price=balance_price)
    else:
        flash("No that client_id!", "error")
        return render_template("info.html", user=current_user, form=form)


@app.route("/info/<int:id>", methods=["GET", "POST"])
def info_id(id):
    form = Mine()
    if form.validate_on_submit:
        exact = Reg.query.get_or_404(id)
        return render_template("info_id.html", form=form, exact=exact, user=current_user)


@app.route("/users")
def users():
    users = User.query.filter_by(email=User.email).all()
    return render_template("users.html", user=current_user, users=users)


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
        if user:
            flash("This email is already have. Use another!", category="error")
        elif len(email) < 5:
            flash("At least 6 characters for email, please!", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 5:
            flash("At least 6 characters for password, please", category="error")
        else:
            new_user = User(email=email, fullname=fullname, comment=comment,
                            password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully!", category="success")
            return redirect(url_for("login"))
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


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("At least 1 characters", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    return render_template("notes.html", user=current_user)


@app.route("/create_all")
def create_all():
    db.create_all()
    return "All tables are created!!!"

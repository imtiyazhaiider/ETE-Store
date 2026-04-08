from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)

ADMIN_EMAIL = "imtiyazhaider00@gmail.com"


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))

        # Make admin automatically if email matches
        is_admin = True if email == ADMIN_EMAIL else False

        user = User(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully!", "success")
        return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            # Ensure admin stays admin
            if user.email == ADMIN_EMAIL:
                user.is_admin = True
                db.session.commit()

            login_user(user)
            return redirect('/')

        flash("Invalid credentials", "danger")

    return render_template("login.html")


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
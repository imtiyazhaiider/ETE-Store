from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

ADMIN_EMAIL = "imtiyazhaider00@gmail.com"


# 🔐 REGISTER
@auth.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # ✅ validation
        if not username or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for('auth.register'))

        # ✅ check existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered", "warning")
            return redirect(url_for('auth.register'))

        # 🔒 hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # 👑 admin auto assign
        is_admin = True if email == ADMIN_EMAIL else False

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            is_admin=is_admin
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template("register.html")


# 🔑 LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            # 👑 ensure admin stays admin
            if user.email == ADMIN_EMAIL and not user.is_admin:
                user.is_admin = True
                db.session.commit()

            login_user(user)

            flash("Login successful!", "success")
            return redirect('/')

        flash("Invalid email or password", "danger")

    return render_template("login.html")


# 🚪 LOGOUT
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))
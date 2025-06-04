from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pw')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Welcome back, {user.first_name}!', 'success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', 'error')
        else:
            flash('Given email is not registered.', 'error')

    return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        pw1 = request.form.get('password1')
        pw2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email is already registered.', 'error')
        elif len(first_name) < 2:
            flash('First name must be at least two characters.', 'error')
        elif len(email) == 0:
            flash('You must enter an email.', 'error')
        elif len(pw1) < 5:
            flash('Your password must be at least 5 characters.', 'error')
        elif re.fullmatch("^(?=.*[0-9])(?=.*[A-Z]).+$", pw1) is None:
            flash('Your password must contain at least one number and one capital letter.', 'error')
        elif pw1 != pw2:
            flash('Passwords don\'t match.', 'error')
        else:
            flash('Your account has been successfully created.', 'success')
            u = User(first_name=first_name, email=email, password=generate_password_hash(pw1, method='pbkdf2:sha256'))
            db.session.add(u)
            db.session.commit()
            login_user(u, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
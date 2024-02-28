from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                error = 'Incorrect password, try again.'
        else:
            error = 'Email does not exist.'

    return render_template("index.html", user=current_user, error=error)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    error=None
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            error = 'Email already exists.'
        elif len(email) < 4:
            error = 'Email must be greater than 3 characters.'
        elif len(first_name) < 2:
            error = 'First name must be greater than 1 character.'
        elif password1 != password2:
            error = 'Passwords don\'t match.'
        elif len(password1) < 7:
            error = 'Password must be at least 7 characters.'
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("index.html", user=current_user, error=error)

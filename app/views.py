from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, CodingForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from app.models import Award, User, Title, Abstract, Project


@app.before_request
def session_management():
    """Initialize Flask session storage to remember skipped awards."""
    session.permanent = True
    if 'skipped_awards' not in session:
        session['skipped_awards'] = []


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

# TODO: Move coding stuff to separate directory



# TODO: Move coding stuff to separate directory



# TODO: Move coding stuff to separate directory



# TODO: Move user stuff to a separate directory



# TODO: Move user stuff to a separate directory



# TODO: Move user stuff to a separate directory



# TODO: Move user stuff to a separate directory


# TODO: Move user stuff to a separate directory

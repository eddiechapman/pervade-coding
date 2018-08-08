from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, CodingForm
from app.models import User, Award

@app.before_request
def session_management():
    session.permanent = True
    if 'skipped_awards' not in session:
        session['skipped_awards'] = []

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/get_award')
@login_required
def get_award():
    award = Award.query.filter(
        Award.timestamp == None,
        ~Award.id.in_(session['skipped_awards'])
    ).first_or_404()
    return redirect(url_for('code_award', award_id=award.id))


@app.route('/skip_award/<int:award_id>')
@login_required
def skip_award(award_id):
    session['skipped_awards'].append(award_id)
    return redirect(url_for('get_award'))


@app.route('/code_award/<int:award_id>', methods=['GET', 'POST'])
@login_required
def code_award(award_id):
    award = Award.query.get(award_id)
    form = CodingForm()
    if form.validate_on_submit():
        award.pervasive_data = form.pervasive_data.data
        award.data_science = form.data_science.data
        award.big_data = form.big_data.data
        award.case_study = form.case_study.data
        award.data_synonyms = form.data_synonyms.data
        award.not_relevant = form.not_relevant.data
        award.timestamp = datetime.utcnow()
        award.user = current_user.username
        db.session.commit()
        flash('Coding data submitted for ' + award.title)
        return redirect(url_for('get_award'))
    return render_template('coding.html', award=award, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
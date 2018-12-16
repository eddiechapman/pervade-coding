from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, CodingForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.email import send_password_reset_email
from app.models import Award, User, Title, Abstract, Project


@app.route('/get_award')
@login_required
def get_award():
    """Retrieve a single award that has not been coded or skipped."""
    award = Award.query.filter(
            # No timestamp (added when coding form is submitted)
            Award.timestamp == None,
            # No skipped awards matching current award ID
            ~Award.id.in_(session['skipped_awards'])
            # 404 error page is returned if no results
            ).first_or_404()
    return redirect(url_for('code_award', award_id=award.id))


@app.route('/skip_award/<int:award_id>')
@login_required
def skip_award(award_id):
    """Add current award ID to list of skipped awards."""
    session['skipped_awards'].append(award_id)
    return redirect(url_for('get_award'))


@app.route('/code_award/<int:award_id>', methods=['GET', 'POST'])
@login_required
def code_award(award_id):
    """Display award data and coding form. Process form submission."""
    award = Award.query.get(award_id)
    form = CodingForm()
    # TODO: probably can't use validate_on_submit anymore...
    if form.validate_on_submit():
        Title(
                project=None,
                user=current_user,
                timestamp=datetime.utcnow(),
                pervasive_data=form.title_pervasive_data.data,
                data_sci=form.title_data_science.data,
                big_data=form.title_big_data.data,
                case_study=form.title_case_study.data,
                data_synonyms=form.title_data_synonyms.data
                )
        Abstract(
                project=None,
                user=current_user,
                timestamp=datetime.utcnow(),
                pervasive_data=form.abstract_pervasive_data.data,
                data_sci=form.abstract_data_science.data,
                big_data=form.abstract_big_data.data,
                case_study=form.abstract_case_study.data,
                data_synonyms=form.abstract_data_synonyms.data
                )
        db.session.commit()
        flash('Coding data submitted.')
        return redirect(url_for('get_award'))
    return render_template('coding.html', award=award, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate login credentials, retrieve user info from database."""
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
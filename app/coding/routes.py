from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, current_app
from flask_login import current_user, login_required
from app import db
from app.coding.forms import CodingForm
from app.models import Award, Code
from app.coding import bp


@bp.before_request
def session_management():
    """Initialize Flask session storage to remember skipped awards."""
    session.permanent = True
    if 'skipped_awards' not in session:
        session['skipped_awards'] = []


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Main landing page."""
    return render_template('index.html')


@bp.route('/get_award')
@login_required
def get_award():
    """Retrieve a single award that has not been coded or skipped.
    
    Returns:
         Redirect to 404 error page if no awards are found.
    """
    award = Award.query.first_or_404()
    while not award.available_for_coding(current_user):
        award = Award.query.first_or_404()
    return redirect(url_for('coding.code_award', award_id=award.id))


@bp.route('/skip_award/<int:award_id>')
@login_required
def skip_award(award_id):
    """Add current award ID to list of skipped awards.
    
    Args:
        award_id (int): The ID of the current award that should be skipped.
    
    Returns:
        Redirect to get_award after skipping current award.
    """
    session['skipped_awards'].append(award_id)
    return redirect(url_for('coding.get_award'))


@bp.route('/code_award/<int:award_id>', methods=['GET', 'POST'])
@login_required
def code_award(award_id):
    """Display award data and coding form. Process form submission.
    
    Args:
        award_id (int): The ID of the current award.
        
    Returns:
        Redirect to coding form on first visit, or a redirect to
            get_award on form submit.
    """
    award = Award.query.get(award_id)
    form = CodingForm()
    if form.validate_on_submit():
        title = Code(code_type='title', time=datetime.utcnow())
        abstract = Code(code_type='abstract', time=datetime.utcnow())
        form.title.populate_obj(title)
        form.abstract.populate_obj(abstract)
        award.codes.extend([title, abstract])
        current_user.codes.extend([title, abstract])
        db.session.commit()
        flash('Coding data submitted.')
        return redirect(url_for('coding.get_award'))
    return render_template('coding/coding.html', award=award, form=form)
from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, current_app
from flask_login import current_user, login_required
from app import db
from app.coding.forms import CodingForm
from app.models import Award, Code
from app.coding import bp




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
    
    awards = Award.query.all()
    for award in awards:
        if not award.codes:
            return redirect(url_for('coding.code_award', award_id=int(award.id)))
        elif len(award.codes) < 3\
            & current_user.id not in [code.user for code in award.codes]:
            return redirect(url_for('coding.code_award', award_id=int(award.id)))


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
    abstract = award.abstract
    abstract_paras = abstract.split('\\n')
    form = CodingForm()
    if form.validate_on_submit():
        title = Code(
            code_type='title',
            pervasive_data=form.pervasive_data_ti.data,
            data_science=form.data_science_ti.data,
            big_data=form.big_data_ti.data,
            case_study=form.case_study_ti.data,
            data_synonyms=form.data_synonyms_ti.data
        )
        title.award = award
        title.user = current_user
        
        abstract = Code(
            code_type='abstract',
            pervasive_data=form.pervasive_data_abs.data,
            data_science=form.data_science_abs.data,
            big_data=form.big_data_abs.data,
            case_study=form.case_study_abs.data,
            data_synonyms=form.data_synonyms_abs.data
        )
        abstract.award = award
        abstract.user = current_user

        db.session.commit()
        flash('Coding data submitted.')
        return redirect(url_for('coding.get_award'))
    return render_template('coding.html', award=award, form=form, abstract_paras=abstract_paras)
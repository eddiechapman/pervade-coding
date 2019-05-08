from datetime import datetime
from flask import render_template, flash, redirect, url_for, session, current_app
from flask_login import current_user, login_required
from sqlalchemy import func
from app import db
from app.coding.forms import CodingForm
from app.models import Award, Code
from app.coding import bp



@bp.route('/')
@bp.route('/index')
@login_required
def index(codes_goal=None, codes_complete=None):
    """
    Main landing page. Fetch the remaining number of awards to be coded.
    """
    coded_once = Award.query.filter_by(len(Award.codes) == 1).count()
    coded_never = Award.query.filter_by(len(Award.codes) == 0).count()
    codes_goal = Award.query.all().count() * 2
    codes_complete = coded_once + (coded_never * 2)
    return render_template('index.html',
                            codes_complete=codes_complete,
                            codes_goal=codes_goal)


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
        elif len(award.codes) == 1:
            for code in award.codes:
                if code.user_id != current_user.id:
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
        code = Code(
            pervasive_data=form.pervasive_data.data,
            data_science=form.data_science.data,
            big_data=form.big_data.data,
            data_synonyms=form.data_synonyms.data,
            comments=form.comments.data
        )
        code.award = award
        code.user = current_user
        db.session.commit()
        flash('Coding data submitted.')
        return redirect(url_for('coding.get_award'))
    return render_template('coding.html', award=award, form=form, abstract_paras=abstract_paras)
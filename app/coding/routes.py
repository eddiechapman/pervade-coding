import csv
import datetime
import io

from flask import (render_template, flash, redirect, url_for,
                   make_response)
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.coding.forms import CodingForm
from app.models import Award, Code
from app.coding import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """
    Main landing page. Fetch the remaining number of awards to be coded.
    """
    total_awards = Award.query.all()
    remaining = 0
    for award in total_awards:
        if len(award.codes) == 0:
            remaining += 2
        elif len(award.codes) == 1:
            remaining += 1
    return render_template('index.html',
                            codes_complete=remaining,
                            codes_goal=len(total_awards))


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
    return render_template('coding.html', award=award,
                            form=form, abstract_paras=abstract_paras)


@bp.route('/export')
@login_required
def export():
    """
    Download coding data in CSV form.
    """
    data = io.StringIO()
    writer = csv.writer(data)
    writer.writerow(('code_id', 'award_id', 'title', 'abstract',
                     'pervasive_data', 'data_science', 'big_data',
                     'data_synonyms', 'comments', 'user_id',
                     'timestamp'))

    for code in Code.query.all():
        writer.writerow((code.id, code.award.award_id,
                         code.award.title, code.award.abstract,
                         code.pervasive_data, code.data_science,
                         code.big_data, code.data_synonyms,
                         code.comments, code.user_id, code.time))

    timestamp = datetime.datetime.today().strftime('%Y-%m-%d')
    filename = f'pervade_coding_export_{timestamp}.csv'

    response = make_response(data.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "text/csv"
    return response



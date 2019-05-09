from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField

class CodingForm(FlaskForm):
    """
    The form for recording coding information about an award.
    """
    pervasive_data = BooleanField(label='Pervasive Data')
    data_science = BooleanField(label='Data Science')
    big_data = BooleanField(label='Big Data')
    comments = TextAreaField(label='Comments')
    data_synonyms = TextAreaField(
        label='Data synonyms',
        description='Please separate values with a semicolon',
    )
    submit = SubmitField(label='Submit')

    def validate(self):
        """
        This should have something more useful but it doesn't work
        otherwise!
        """
        return True
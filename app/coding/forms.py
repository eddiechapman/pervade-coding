from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField

class CodingForm(FlaskForm):
    """The form for recording coding information about an award."""
    pervasive_data = BooleanField('Pervasive Data')
    data_science = BooleanField('Data Science')
    big_data = BooleanField('Big Data')
    comments = TextAreaField('Comments')
    data_synonyms = TextAreaField('Data synonyms', description='Please separate values with a semicolon')
    submit = SubmitField('Submit')

    def validate(self):
        """This should have something more useful but it doesn't work otherwise."""
        return True
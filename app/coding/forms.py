from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField, StringField

class CodingForm(FlaskForm):
    """Groups the coding forms for an award so they can be submitted together.
    
    Attributes:
        title_codes: A form for coding the award's title.
        abstract_codes: A form for coding the award's abstract.
        submit: A button for submitting all the form data.
    """

    # Title fields
    case_study_ti = BooleanField('Flag for PRIM&R case study')
    pervasive_data_ti = BooleanField('Pervasive Data')
    data_science_ti = BooleanField('Data Science')
    big_data_ti = BooleanField('Big Data')
    data_synonyms_ti = StringField('Data synonyms',
                                     description='Please separate values with a semicolon')
    # Abstract fields
    case_study_abs = BooleanField('PRIM&R case study')
    pervasive_data_abs = BooleanField('Pervasive Data')
    data_science_abs = BooleanField('Data Science')
    big_data_abs = BooleanField('Big Data')
    data_synonyms_abs = TextAreaField('Data synonyms',
                                      description='Please separate values with a semicolon')
    submit = SubmitField('Submit')
    
    def validate(self):
        return True
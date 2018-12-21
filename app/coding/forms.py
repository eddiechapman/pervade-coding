from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, TextAreaField, SelectMultipleField, FormField
from wtforms.validators import Length


class CodeSection(FlaskForm):
    """A group of fields for coding a section of an award.
    
    Can be used for either the title or the abstract.
    
    Attributes:
        themes: Allows the user to pick multiple themes that represent the award.
        case_study: Should the award be included in a future case study event?
        synoyms: A free text field for listing synonyms for data.
        
    Raises:
        ValidationError: If the synonyms field exceeds 500 characters.
    """
    case_study = BooleanField('Flag for PRIM&R case study')
    pervasive_data = BooleanField('Pervasive Data')
    data_science = BooleanField('Data Science')
    big_data = BooleanField('Big Data')
    data_synonyms = TextAreaField('Data synonyms',
                              description='Please separate values with a semicolon',
                              validators=[Length(min=0, max=500)] )


class CodingForm(FlaskForm):
    """Groups the coding forms for an award so they can be submitted together.
    
    Attributes:
        title_codes: A form for coding the award's title.
        abstract_codes: A form for coding the award's abstract.
        submit: A button for submitting all the form data.
    """
    title_codes = FormField(CodeSection, separator='Title')
    abstract_codes = FormField(CodeSection, separator='Abstract')
    submit = SubmitField('Submit')
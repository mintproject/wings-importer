# -*- coding: utf-8 -*-
"""Server forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

<<<<<<< HEAD

class ImportComponentForm(FlaskForm):
    """Register form."""
=======
class ImportComponentForm(FlaskForm):
    """Register form."""
    #componente
>>>>>>> 47e133b05d542f00041d3550f6069d4c069ab495

    component = StringField('Instance URI',
                           validators=[DataRequired(), Length(min=3, max=256)])
    server = SelectField(u'Server configuration', choices=[], coerce=int)
<<<<<<< HEAD
    wings_username = StringField('WINGS username',
                           validators=[DataRequired(), Length(min=3, max=80)])
    wings_password = PasswordField('WINGS user password',
                           validators=[DataRequired(), Length(min=3, max=128)])
    wings_domain = StringField('WINGS domain',
                           validators=[DataRequired(), Length(min=3, max=80)])
=======
>>>>>>> 47e133b05d542f00041d3550f6069d4c069ab495

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ImportComponentForm, self).__init__(*args, **kwargs)

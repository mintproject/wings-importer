# -*- coding: utf-8 -*-
"""Server forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class ImportComponentForm(FlaskForm):
    """Register form."""
    #componente

    component = StringField('Instance URI',
                           validators=[DataRequired(), Length(min=3, max=256)])
    server = SelectField(u'Server configuration', choices=[], coerce=int)

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ImportComponentForm, self).__init__(*args, **kwargs)

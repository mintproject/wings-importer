# -*- coding: utf-8 -*-
"""Server forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ImportComponentForm(FlaskForm):
    """Register form."""

    component = StringField('Instance URI',
                           validators=[DataRequired(), Length(min=3, max=256)])
    server = SelectField(u'Server configuration', choices=[], coerce=int)
    wings_username = StringField('WINGS username',
                           validators=[DataRequired(), Length(min=3, max=80)])
    wings_password = PasswordField('WINGS user password',
                           validators=[DataRequired(), Length(min=3, max=128)])
    wings_domain = StringField('WINGS domain',
                           validators=[DataRequired(), Length(min=3, max=80)])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ImportComponentForm, self).__init__(*args, **kwargs)

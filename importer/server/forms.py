# -*- coding: utf-8 -*-
"""Server forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length

from .models import Server


class AddForm(FlaskForm):
    """Register form."""

    server_name = StringField('Configuration Name',
                           validators=[DataRequired(), Length(min=3, max=256)])
    server_wings = StringField('WINGS uri',
                           validators=[DataRequired(), Length(min=3, max=256)])
    server_mint = StringField('MINT uri',
                           validators=[DataRequired(), Length(min=3, max=256)])
    endpoint_mint = StringField('MINT endpoint',
                           validators=[DataRequired(), Length(min=3, max=256)])
    wings_exporturl = StringField('WINGS export url',
                           validators=[DataRequired(), Length(min=3, max=256)])
    is_public = BooleanField('Is public?',
                            validators=[DataRequired()])


    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AddForm, self).__init__(*args, **kwargs)
        self.user = None


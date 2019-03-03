# -*- coding: utf-8 -*-
"""Server forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

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
    wings_username = StringField('WINGS username',
                           validators=[DataRequired(), Length(min=3, max=80)])
    wings_password = PasswordField('WINGS user password',
                           validators=[DataRequired(), Length(min=3, max=128)])
    wings_exporturl = StringField('WINGS export url',
                           validators=[DataRequired(), Length(min=3, max=256)])


    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AddForm, self).__init__(*args, **kwargs)
        self.user = None


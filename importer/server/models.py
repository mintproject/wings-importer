# -*- coding: utf-8 -*-
"""server models."""
import datetime as dt

from importer.database import Column, Model, SurrogatePK, db, reference_col, relationship
from importer.extensions import bcrypt


class Server(SurrogatePK, Model):
    """A server of the app."""

    __tablename__ = 'servers'
    server_name = Column(db.Integer, nullable=False)
    server_wings = Column(db.String(256), nullable=False)
    server_mint = Column(db.String(256), nullable=False)
    endpoint_mint = Column(db.String(256), nullable=False)
    wings_exporturl = Column(db.String(256), nullable=False)
    is_public = Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, server_name, server_wings, server_mint, endpoint_mint,
                 wings_exporturl, is_public, user, **kwargs):
        """Create instance."""
        db.Model.__init__(self, server_name=server_name, server_wings=server_wings,
                          server_mint=server_mint, endpoint_mint=endpoint_mint,
                          wings_exporturl=wings_exporturl, is_public=is_public,
                          user=user)

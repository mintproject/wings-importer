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
    wings_username = Column(db.String(80), nullable=False)
    wings_password = Column(db.Binary(128), nullable=True)
    wings_exporturl = Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, server_name, server_wings, server_mint, endpoint_mint,
        wings_username, wings_password, wings_exporturl, user, **kwargs):
        """Create instance."""
        db.Model.__init__(self, server_name=server_name, server_wings=server_wings, 
            server_mint=server_mint, endpoint_mint= endpoint_mint,
            wings_username=wings_username,  wings_exporturl=wings_exporturl, 
            user=user, **kwargs)
        if wings_password:
            self.set_password(wings_password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.wings_password, value)

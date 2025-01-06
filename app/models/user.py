from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..extensions import db


class User(db.Model):
    __tablename__ = 'users'

    username = Column(String(80), primary_key=True, nullable=False)
    password = Column(String(80), nullable=False)

    files = relationship('UserFiles', back_populates='user')
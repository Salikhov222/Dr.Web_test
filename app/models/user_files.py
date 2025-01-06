from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..extensions import db


class UserFiles(db.Model):
    __tablename__ = 'user_files'

    user_username = Column(String(80), ForeignKey('users.username'), primary_key=True, nullable=False)
    file_hash = Column(String(255), ForeignKey('files.hash'), primary_key=True, nullable=False)

    user = relationship('User', back_populates='files')
    file = relationship('File', back_populates='users')
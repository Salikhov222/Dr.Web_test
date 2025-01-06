from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ..extensions import db


class File(db.Model):
    __tablename__ = 'files'

    hash = Column(String(255), nullable=False, primary_key=True)
    file_extension = Column(String(255), nullable=False)

    users = relationship('UserFiles', back_populates='file')
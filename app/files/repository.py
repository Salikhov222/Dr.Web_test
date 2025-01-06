from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app

from ..models.user import User
from ..models.file import File
from ..models.user_files import UserFiles


class FileRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, file: File):
        try:
            self.db_session.add(file)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            current_app.logger.exception(f"Failed to add file {e}")
            raise

    def add_user_file(self, user_file: UserFiles):
        try:
            self.db_session.add(user_file)
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            current_app.logger.exception(f"Failed to add file {e}")
            raise

    def get_by_hash(self, file_hash: str) -> File:
        return self.db_session.query(File).filter_by(hash=file_hash).first()

    def get_user(self, username: str) -> User:
        return self.db_session.query(User).filter_by(username=username).first()

    def get_user_file(self, username: str, file_hash: str) -> UserFiles:
        return self.db_session.query(UserFiles).filter_by(user_username=username, file_hash=file_hash).first()

    def delete_user_file(self, user: User, file: File):
        try:
            self.db_session.query(UserFiles).filter_by(user_username=user.username, file_hash=file.hash).delete()
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            current_app.logger.exception(f"Failed to remove file {e}")
            raise

    def delete(self, file_hash: str):
        try:
            self.db_session.query(File).filter_by(hash=file_hash).delete()
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            current_app.logger.exception(f"Failed to delete file {e}")
            raise
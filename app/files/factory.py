from .service import FileService
from .repository import FileRepository


def create_file_service(db_session):
    return FileService(FileRepository(db_session))
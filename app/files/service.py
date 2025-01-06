import hashlib
import os
from flask import send_from_directory, current_app

from ..config import config
from .repository import FileRepository
from ..models.file import File
from ..models.user_files import UserFiles


class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    def get_file(self, file_hash: str):
        """
        Return file by hash
        """
        file = self.file_repository.get_by_hash(file_hash)
        if file is None:
            raise FileNotFoundError('File Not Found')
        filename = file_hash + file.file_extension
        directory_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_hash[:2])
        return send_from_directory(directory_path, filename, as_attachment=True)

    def save_file(self, file, username: str) -> str:
        """
        Save uploaded file and associate it with user
        """
        file_content = file.read()
        file_hash = self._generate_file_hash(file_content)
        _, file_extension = os.path.splitext(file.filename)

        existing_file = self.file_repository.get_by_hash(file_hash)
        if existing_file:
            # Проверяем, существует ли уже связь этого пользователя с файлом
            user_file = self.file_repository.get_user_file(username, file_hash)
            if not user_file:
                # Если файл уже существует, возвращаем хэш, привязываем к новому юзеру и не сохраняем в хранилище
                user_file = UserFiles(
                    user_username=username,
                    file_hash=file_hash,
                )
                self.file_repository.add_user_file(user_file)
                return file_hash
            else:
                raise FileExistsError('File Already Exists')

        file_name = f"{file_hash}{file_extension}"
        file_path = os.path.join(config.STORAGE_FOLDER, file_hash[:2], file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_content)

        new_file = File(
            hash=file_hash,
            file_extension=file_extension,
        )
        user_file = UserFiles(
            user_username=username,
            file_hash=file_hash,
        )
        self.file_repository.add(new_file)
        self.file_repository.add_user_file(user_file)

        return file_hash

    def delete_file(self, file_hash: str, username: str):
        """
         Delete a file associated with the user by its hash.
        """
        file = self.file_repository.get_by_hash(file_hash)
        user = self.file_repository.get_user(username)

        if not file:
            raise FileNotFoundError('File Not Found')
        # Получаем все хэши файлов, связанных с пользователем
        user_file_hashes = [user_file.file_hash for user_file in user.files]

        if file.hash not in user_file_hashes:
            raise PermissionError('User Not Found')

        # Удаляем связь между пользователем и файлом
        self.file_repository.delete_user_file(user, file)

        if not file.users:
            directory_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_hash[:2])
            os.remove(os.path.join(directory_path, file_hash + file.file_extension))
            self.file_repository.delete(file_hash)

        return file_hash

    @staticmethod
    def _generate_file_hash(file_content: bytes) -> str:
        """
        Generate a unique file hash
        """
        return hashlib.sha256(file_content).hexdigest()
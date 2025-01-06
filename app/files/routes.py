from flask_restx import Resource, Namespace
from flask import request
from werkzeug.datastructures import FileStorage

from ..extensions import db
from .utils import authorize_user
from .factory import create_file_service


files_namespace = Namespace('files', description='Files related operations')
upload_parser = files_namespace.parser()
upload_parser.add_argument('file', type=FileStorage, location='files', help='File to upload', required=True)

@files_namespace.route('/<string:file_hash>')
class FileManager(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_service = create_file_service(db.session)

    @files_namespace.doc(
        "Download a file by its hash",
        responses={
            200: "File successfully sent",
            404: "File not found!",
        },
    )
    def get(self, file_hash):
        """
        Download a file by its hash
        :param file_hash: The hash of the file to download
        :return: The file if found, otherwise an error message
        """
        return self.file_service.get_file(file_hash)

    @files_namespace.doc(security='basicAuth')
    @authorize_user
    @files_namespace.doc(
        " Delete a file by its hash",
        responses={
            200: "File successfully deleted",
            401: "Unauthorized",
            403: "Permission error",
            404: "File not found!",
        },
    )
    def delete(self, file_hash):
        """
        Delete a file by its hash
        :param file_hash: The hash of the file to delete
        :return: Success or error message
        """
        username = request.authorization['username']
        file_hash = self.file_service.delete_file(file_hash, username)
        return {"message": f"File {file_hash} delete successfully"}, 200

@files_namespace.route('/')
@files_namespace.expect(upload_parser)
class FileUpload(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_service = create_file_service(db.session)

    @files_namespace.doc(security='basicAuth', consumes=["multipart/form-data"])
    @authorize_user
    @files_namespace.doc(
        "Upload a new file",
        responses={
            200: "File successfully uploaded",
            401: "Unauthorized",
        },
    )
    def post(self):
        """
        Upload a new file
        :return: The hash of the uploaded file
        """
        args = upload_parser.parse_args()  # Парсим входные данные
        uploaded_file = args['file']  # Получаем загруженный файл как FileStorage
        username = request.authorization['username']
        file_hash = self.file_service.save_file(uploaded_file, username)
        return {"file_hash": file_hash}, 201



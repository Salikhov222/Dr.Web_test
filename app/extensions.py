from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

from sqlalchemy.exc import SQLAlchemyError


authorizations = {
    "basicAuth": {
        "type": "basic",
    }
}

api = Api(doc="/docs",
          title="File Storage API",
          version="1.0",
          description="API для загрузки, скачивания и удаления файлов",
          authorizations=authorizations,
      )

db = SQLAlchemy()
migrate = Migrate()

def register_error_handlers(api: Api):
    @api.errorhandler(FileNotFoundError)
    def handle_file_not_found_error(error):
        return {"message": str(error)}, 404

    @api.errorhandler(PermissionError)
    def handle_permission_error(error):
        return {"message": str(error)}, 403

    @api.errorhandler(FileExistsError)
    def handle_file_exists_error(error):
        return {"message": str(error)}, 400

    @api.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        return {"message": "A database error occurred."}, 500

    @api.errorhandler(Exception)
    def handle_unexpected_error(error):
        return {"message": "An unexpected error occurred.", "details": str(error)}, 500
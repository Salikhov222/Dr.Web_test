from functools import wraps
from flask import request
from ..models.user import User, db


def authorize_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return {"message": "Unauthorized"}, 401

        user = db.session.query(User).filter_by(username=auth.username, password=auth.password).first()
        if not user:
            return {"message": "Invalid credentials"}, 401

        return f(*args, **kwargs)
    return decorated_function
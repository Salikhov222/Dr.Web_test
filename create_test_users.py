from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    if not User.query.first():  # Проверяем, есть ли пользователи в базе
        users = [
            User(username="admin", password="admin"),
            User(username="guest", password="guest")
        ]
        db.session.add_all(users)
        db.session.commit()
        print("Test users created!")
    else:
        print("Users already exist!")
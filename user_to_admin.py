from app.models import User
from app import db


def user_to_admin(user):
    user.role = 2
    db.session.commit()


if __name__ == "__main__":
    user = User.query.get(1)
    if user:
        user_to_admin(user)
        print(f"Пользователь {user.username} теперь администратор.")
    else:
        print(f"Пользователь с таким id не найден.")

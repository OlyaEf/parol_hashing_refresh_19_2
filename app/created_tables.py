from app.config import Config
from app.dao.model.user import User
from app.database import db


from main import create_app


if __name__ == '__main__':
    with create_app(Config).app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])

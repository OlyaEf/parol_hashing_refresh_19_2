# Временное хранилище наших сервисов и дополнительных объектов кторые нужно
# где-то инициализировать. Сервис-контейнер


from app.dao.user import UserDAO
from app.database import db
from app.services.user import UserService


# создаем автор дао. Дао в качестве зависимости получает сессию.
user_dao = UserDAO(db.session)
# инициализируем автор_сервис. Указываем автор дао в качестве зависимости.
user_service = UserService(user_dao)

# auth_dao = AuthDao(db.session)
# auth_services = AuthService(auth_dao)
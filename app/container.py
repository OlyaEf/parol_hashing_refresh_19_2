# Временное хранилище наших сервисов и дополнительных объектов кторые нужно
# где-то инициализировать. Сервис-контейнер


from app.dao.user import UserDAO
from app.database import db
from app.services.auth import AuthService
from app.services.user import UserService


# создаем автор дао. Дао в качестве зависимости получает сессию.
user_dao = UserDAO(db.session)

# Инициализируем автор_сервис. Указываем автор дао в качестве зависимости.
user_service = UserService(user_dao)


auth_services = AuthService(user_service)

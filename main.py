# main.py

# Импорт необходимых библиотек
from flask import Flask
from flask_restx import Api

# импортируем класс Config
from app.config import Config
from app.dao.model.user import User

# импортируем db из нашего нового файла
from app.database import db
from app.views.auth import auth_ns
# подключаем наши модели для работы функции def load_data()

# подключаем namespace book_ns, author_ns
from app.views.users import user_ns


# def create_app() - создает приложение и возвращает его.
# Передадим функции аргумент. Научим ее работать с конфиг.
def create_app(config: Config) -> Flask:
    # создаем app, называем ее application что бы оно не пересекалось с app
    app = Flask(__name__)
    # создаем конфигурацию, вызвав у нее специальный метод from_object
    app.config.from_object(config)  # это и есть наш конфиг класса class Config
    # Применение конфигурации которую мы настроили выше, чтобы Flask обновил ее по всему приложению.
    app.app_context().push()

    # вызываем метод configure_app() что бы метод заработал (конфигурируем приложение).
    configure_app(app)  # передаем ему приложение.

    return app


# Конфигурируем создание объекта db = SQLAlchemy(). Связь расположения объектов.
def configure_app(app: Flask):
    # подключает базу данных.
    db.init_app(app)
    # создаем объект API.
    api = Api(app)
    # добавление неймспейсов, которые нам будут переданы.
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


# при создании приложения мы грузим некоторый набор данных
def load_data():
    # создаем нового пользоватаеля, у которого юзернейм-рут, пароль - какой-то рандомный пароль, роль - админ.
    user = User(username='root', password='random_password', role='admin')

    # Создаем необходимые таблицы
    db.create_all()

    # При помощи открытия сессии сохраняем наши данные в базе
    with db.session.begin():
        db.session.add_all([user])


# Загружаем конфигурацию.
app_config = Config()  # здесь храниться конфигурация.
# Создаем приложение. Передаем в функцию 'создания приложения' - 'экземпляр класса конфигурации'.
app = create_app(app_config)  # здесь храниться приложение.


# загрузка данных для создания таблиц.
load_data()


# Запуск приложения. Если файл исполняемый:
if __name__ == '__main__':
    # Запускаем приложение.
    app.run()

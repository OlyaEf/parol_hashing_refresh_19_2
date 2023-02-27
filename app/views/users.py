# Преставление user.py

# научим вью работать с моделью, но не используя напрямую внешние зависимости такие как session, query, и т.д.
# взаимодействовать модель и представление будет через класс DAO


from flask import request
from flask_restx import Resource, Namespace

from app.container import user_service
from app.dao.model.user import UserSchema
from app.helpers.decorators import admin_required

# Создание неймспейса.
user_ns = Namespace('users')

# Схема объект для сериализации и десериализации экземпляров.
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Интерфейсы для авторов
@user_ns.route('/')  # на адрес / + authors +/
class UsersView(Resource):
    def get(self):
        # направляем get запрос через наше DAO
        users = user_service.get_all()
        response = UserSchema(many=True).dump(users)
        return response, 200

    def post(self):
        # направляем новую форму
        data = request.json
        # создаем пользователя через DAO используя метод create
        user = user_service.create(data)
        # возвращаем заголовок - location
        return "", 201, {'location': f'/user/{user.id}'}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    # get продолжает получать некоторый индетификатор.
    def get(self, uid: int):  # Получение данных
        try:
            # получаем объект, где запись id = uid который мы получили
            user = user_service.get_one(uid)
            # получив сущность мы ее сериализуем и отдаем с кодом 200
            return user_schema.dump(user), 200
        except Exception as e:
            #  выводим для примера текстовое обозначение ошибки и код 404
            return str(e), 404

    # для обновления используем метод put, который принимает uid
    def put(self, uid: int):  # Замена данных
        # забирает реквест в формате json
        req_jsoon = request.json
        # получаем uid
        req_jsoon['id'] = uid

        # выполняем замену через метод dao
        user_service.update(req_jsoon)
        return '', 204

    def patch(self, uid: int):  # Частичное обновление
        # забирает реквест в формате json
        req_json = request.json
        req_json['id'] = uid
        # выполняем частичную замену через метод класса dao
        user_service.update_partial(req_json)
        # возвращаем пустую строку и код
        return '', 204

    # используем в качестве декоратора у маршрута удаления пользователя
    @admin_required
    def delete(self, uid: int):  # Удаление записи
        # Вызываем запись по методу делит из класса
        # dao куда прокидываем нащ uid
        user_service.delete(uid)

        return '', 204


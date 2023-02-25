from flask import request
from flask_restx import Namespace, Resource

from app.container import auth_services


auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthsView(Resource):
    # при получении запроса
    def post(self):
        """
        Метод получает токены от пользователя.
        """
        # берем информацию из нашего запроса, из request.json
        # и, складываем ее в дата
        data = request.json

        # получаем два значения пользователь и пароль
        username = data.get('username', None)
        password = data.get('password', None)

        # проверяем что бы они были заполнены
        if None is [username, password]:
            return '', 400

        # если все ок - вызываем аут_сервис и метод генерацтт токена.
        tokens = auth_services.generate_tokens(username, password)

        return tokens, 201

    def put(self):
        """
        Метод позволяет авторизовать пользователя без логина и пароля,
        при наличии одного поля refresh_token.
        """
        data = request.json
        token = data.get('refresh_token')

        tokens = auth_services.approve_refresh_token(token)

        return tokens, 201

from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from migrations.db_login import getUser, readUser
import requests
import sys
import json
from config import Config

class LoginForm(FlaskForm):
    """
        Класс формы авторизации
    """
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class UserLogin:
    """
        Класс для получения
            информации из формы авторизации
    """
    def fromDB(self, user_id):
        self.__user = getUser(user_id)[0]
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user)


class LoginVerification:
    """
        Класс для проверки
                логина, пароля и капчи
    """

    def __init__(self):
        ...

    def verification(self, username: str, psw: str) -> bool:
        """
            Проверка на совпадение паролей
        """
        req = readUser()
        print(req)
        saved_psw = req.psw
        saved_username = req.user
        if check_password_hash(saved_psw, psw) and username == saved_username:
            return True
        else:
            return False

    def check_captcha(self, token: str, ip_addr: str):
        """
            Функция, которая проверяет
                капчу в форме авторизации
        """
        resp = requests.get(
            "https://captcha-api.yandex.ru/validate",
            {
                "secret": Config.SMARTCAPTCHA_SERVER_KEY_2,
                "token": token,
                "ip": ip_addr
            },
            timeout=1
        )
        server_output = resp.content.decode()
        if resp.status_code != 200:
            print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
            return True
        return json.loads(server_output)["status"] == "ok"
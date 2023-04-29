from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import flash
import requests
import sys
import json
from config import Config
from migrations.tables import FeedbackT
from migrations.data_base import DataBase


class FeedbackForm(FlaskForm):
    """
        Класс формы обратной связи
    """
    email = StringField('Email*', validators=[DataRequired()])
    number = StringField('Номер телефона', validators=[])
    comment = TextAreaField('Комментарий*', validators=[DataRequired()])
    submit = SubmitField('Отправить отзыв')


class FeedbackManager:
    """
        Класс для работы
            с обратной связью
    """

    def add_new_feedback(self, data: dict) -> bool:
        """
            Функция, которая записывает
                данные из формы обратной связи
        """
        anm = DataBase(FeedbackT)
        anm.session.add(FeedbackT(**anm.filter_request(**data)))
        if anm.session.new:
            anm.session.commit()
            return True
        return False


    def get_admin_feedback(self):
        """
            Функция, которая отправляет
                в панель администратора весь фидбек
        """
        gma = DataBase(FeedbackT)
        data = gma.gettuple(gma.query.order_by(gma.desc(FeedbackT.id)).all())
        if data:
            return data if isinstance(data, list) else [data]
        return []


    def delete_feedback(self, id: str):
        """
            Функция, которая удаляет
                                один отзыв
        """
        dm = DataBase(FeedbackT)
        dm.session.delete(dm.query.filter(FeedbackT.id == id).one())
        dm.session.commit()
        flash(f'Отзыв №{id} успешно удален!')

    def check_captcha(self, token: str, ip_addr: str):
        """
            Функция, которая проверяет
                капчу в форме обратной связи
        """
        resp = requests.get(
            "https://captcha-api.yandex.ru/validate",
            {
                "secret": Config.SMARTCAPTCHA_SERVER_KEY_1,
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


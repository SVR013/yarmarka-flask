from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask import flash
from flask_wtf.file import FileField
from wtforms import SubmitField
from migrations.data_base import DataBase

from migrations.tables import PostsT

photos = ''


class NewsForm(FlaskForm):
    """
        Класс формы обратной связи
    """
    img = FileField('Загрузите фотографию', validators=[DataRequired()])
    url = StringField('Ссылка на статью для url', validators=[DataRequired()])
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Текст статьи', validators=[DataRequired()])
    submit = SubmitField('Добавить новость')


class NewsManager:
    """
        Класс для работы с новостями
    """

    def add_new_post(self, data: dict, img: str) -> bool:
        """
            Функция, которая записывает
                данные из формы добавления новости
        """
        data.update(img=img)

        anm = DataBase(PostsT)
        anm.session.add(PostsT(**anm.filter_request(**data)))
        if anm.session.new:
            anm.session.commit()
            return True
        return False

    def show_news(self, url):
        """
            Функция, которая получает
                новость из бд и формирует словарь
        """
        sm = DataBase(PostsT)
        data = sm.gettuple(sm.query.where(PostsT.url == url).all())
        return data

    def update_news(self, url, title, text, img):
        """
            Функция, которая
                отправляет в бд обновленную новость
        """
        try:
            um = DataBase(PostsT)
            um.query.filter(PostsT.url == url).update({'url': url,
                                                       'title': title,
                                                       'text': text,
                                                       'img': img})
            um.session.commit()
            flash('Пост обновлен успешно!')
            return True
        except:
            return False

    def get_news_anonnce(self):
        """
            Функция, которая
                получает все новости из бд
        """
        gma = DataBase(PostsT)
        data = gma.gettuple(gma.query.order_by(gma.desc(PostsT.url)).all())
        print(data)
        if data:
            return data if isinstance(data, list) else [data]
        return []

    def delete_news(self, url):
        """
            Функция, которая
                удаляет конктретную новость
        """
        dm = DataBase(PostsT)
        dm.session.delete(dm.query.filter(PostsT.url == url).one())
        dm.session.commit()

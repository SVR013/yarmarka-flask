from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask import flash
from flask_wtf.file import FileField
from wtforms import SubmitField
from migrations.data_base import DataBase
from migrations.tables import MembersT


class MembersForm(FlaskForm):
    """
        Класс формы обратной связи
    """
    img = FileField('Загрузите фотографию', validators=[DataRequired()])
    pavilion = StringField('Номер павильона', validators=[DataRequired()])
    title = StringField('Имя участнка', validators=[DataRequired()])
    text = TextAreaField('Описание участника', validators=[DataRequired()])
    submit = SubmitField('Добавить участника')


class MembersManager:

    def add_new_members(self, data: dict, img: str) -> bool:
        """
            Функция, которая записывает
                данные из формы добавления новости
        """
        data.update(img=img)

        anm = DataBase(MembersT)
        anm.session.add(MembersT(**anm.filter_request(**data)))
        if anm.session.new:
            anm.session.commit()
            return True
        return False

    def show_member(self, pavilion):
        """
            Функция, которая получает
                участника из бд и формирует словарь
        """
        sm = DataBase(MembersT)
        data = sm.gettuple(sm.query.where(MembersT.pavilion == pavilion).all())
        return data

    def update_member(self, pavilion, title, text, img):
        """
            Функция, которая
                отправляет в бд обновленного участника
        """
        try:
            um = DataBase(MembersT)
            um.query.filter(MembersT.pavilion == pavilion).update({'pavilion': pavilion,
                                                                   'title': title,
                                                                   'text': text,
                                                                   'img': img})
            um.session.commit()

            flash('Пост обновлен успешно!')
            return True
        except:
            return False

    def get_members_anonnce(self):
        """
            Функция, которая
                получает всех участников из бд
        """
        gma = DataBase(MembersT)
        data = gma.gettuple(gma.query.order_by(gma.desc(MembersT.pavilion)).all())
        if data:
            return data if isinstance(data, list) else [data]
        return []

    def delete_members(self, pavilion):
        """
            Функция, которая
                удаляет конкретного участника
        """
        dm = DataBase(MembersT)
        dm.session.delete(dm.query.filter(MembersT.pavilion == pavilion).one())
        dm.session.commit()

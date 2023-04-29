from flask import render_template, make_response, redirect, url_for, flash, request
from flask_restful import Resource
from models.authorization import LoginForm, LoginVerification, UserLogin
from flask_login import login_user
from models.file_manager import FileManager
from models.feedback import FeedbackManager, FeedbackForm
from models.news_manager import NewsManager
from models.members import MembersManager

from migrations.data_base import DataBase
from migrations.tables import MainPageT, FeedbackT

HEADERS = {'Content-Type': 'text/html'}

class Index(Resource):
    """
        Обработчик для главной страницы
    """
    def get(self):
        theme = 5
        news = NewsManager()
        mb = MembersManager()
        main_news = news.get_news_anonnce()[:3]
        main_members = mb.get_members_anonnce()[:8]
        path = 'gallery'
        gallery = FileManager(path)
        db = DataBase(MainPageT)
        mp_info = db.gettuple(db.query.filter(db.Table.id == '1').all())

        return make_response(
            render_template('master.html', gallery=gallery, members=main_members, theme=theme, db=mp_info,
                            news=main_news),
            200, HEADERS)


class News(Resource):
    """
        Обработчик для страницы новостей
    """
    def get(self):
        news = NewsManager()
        all_news = news.get_news_anonnce()
        return make_response(render_template('news.html', news=all_news), 200, HEADERS)


class GetThere(Resource):
    """
        Обработчик для страницы с местоположением
    """
    def get(self):
        return make_response(render_template('map.html'), 200, HEADERS)


class Gallery(Resource):
    """
        Обработчик для страницы с галереей
    """
    def get(self, path=''):
        gallery = FileManager(path)
        return make_response(render_template('Page-7.html', size=2, gallery=gallery), 200,
                             HEADERS)


class ImageViewer(Resource):
    """
        Обработчик для страницы с фотографией
    """
    def get(self, path='', file=''):
        gallery = FileManager(path)
        next_files = [file]
        if gallery.img:
            i = gallery.img.index(file)
            next_files = gallery.img[i + 1:] + gallery.img[:i]
        return make_response(render_template('seeimg.html', gallery=gallery, file=file, files=next_files), 200, HEADERS)


class LoginPage(Resource):
    """
        Обработчик для страницы с авторизацией
    """
    def __init__(self):
        self.form = LoginForm()
        self.vl = LoginVerification()
        self.ip_addr = request.remote_addr

    def get(self):
        return make_response(render_template('login.html', title='Sign In', form=self.form), 200, HEADERS)

    def post(self):
        token = request.form["smart-token"]
        if self.vl.verification(self.form.username.data, self.form.password.data):  # and self.vl.check_captcha(token, ip_addr):
            userlogin = UserLogin().create(self.form.username.data)
            login_user(userlogin)
            return redirect(url_for('aindex'))
        else:
            flash('Неправильный логин или пароль')
        return make_response(render_template('login.html', form=self.form), 200, HEADERS)


class Feedback(Resource):
    """
        Обработчик для страницы
            с формой обратной связи
    """
    def __init__(self):
        self.form = FeedbackForm()
        self.fb = FeedbackManager()
        self.ip_addr = request.remote_addr

    def get(self):
        return make_response(render_template('feedback.html', form=self.form), 200, HEADERS)

    def post(self):
        form = FeedbackForm()
        if True:
            res = True
            print(form.data)

            fb = DataBase(FeedbackT)
            fb.session.add(fb.Table(email=form.data['email'], number=form.data['number'], comment=form.data['comment']))
            fb.session.commit()
        token = request.form["smart-token"]
        if self.form.validate_on_submit():  # and self.fb.check_captcha(token, ip_addr):
            res = self.fb.add_new_feedback(self.form.data)
            if res:
                flash('Ваш отзыв отправлен, спасибо!', category='success')
                return redirect(url_for('feedback'))
        else:
            flash('Вы указали неверную информацию', category='danger')
            return make_response(render_template('feedback.html', form=self.form), 200, HEADERS)


class ShowNews(Resource):
    """
        Обработчик для страницы с конкретной новостью
    """
    def get(self, url=''):
        news = NewsManager()
        news_page = news.show_news(url)
        news_page['text'] = news_page['text'].split('\n')
        return make_response(render_template('post.html', news=news_page), 200, HEADERS)


class Members(Resource):
    """
        Обработчик для страницы с участниками
    """
    def get(self):
        mb = MembersManager()
        all_members = mb.get_members_anonnce()
        return make_response(render_template('all_members.html', members=all_members), 200, HEADERS)


class ShowMembers(Resource):
    """
        Обработчик для страницы с конкретным участником
    """
    def get(self, pavilion=''):
        mb = MembersManager()
        members_page = mb.show_member(pavilion)
        return make_response(render_template('member.html', members=members_page), 200, HEADERS)

from flask import render_template, make_response, request, redirect, url_for, flash
from flask_restful import Resource
from flask_login import login_required
from models.file_manager import FileManager
from models.feedback import FeedbackManager
from models.news_manager import NewsManager, NewsForm
from models.members import MembersForm, MembersManager
from migrations.data_base import DataBase
from migrations.tables import MainPageT

HEADERS = {'Content-Type': 'text/html'}


class AIndex(Resource):
    """
        Обработчик для страницы
                с панелью управления
    """

    @login_required
    def get(self):
        db = DataBase(MainPageT)
        mp_info = db.gettuple(db.query.filter(db.Table.id == '1').all())
        return make_response(render_template('admin_index.html', db=mp_info), 200, HEADERS)

    @login_required
    def post(self):
        db = DataBase(MainPageT)
        f_manager = FileManager('bg')

        req = dict(request.form.items())
        if req:
            db.query.filter(db.Table.id == '1').update(req)
            db.session.commit()
        req = dict(request.files.items())
        if req:
            file = [req['file']]
            f_manager.add_img(file, resize=False)
        mp_info = db.gettuple(db.query.filter(db.Table.id == '1').all())
        return make_response(render_template('admin_index.html', db=mp_info), 200, HEADERS)


class ANews(Resource):
    """
        Обработчик для страницы
            с редактированием новостей
    """

    def __init__(self):
        self.form = NewsForm()
        self.path = 'posts'
        self.f_manager = FileManager(self.path)

    @login_required
    def get(self):
        return make_response(render_template('admin_news.html', form=self.form), 200, HEADERS)

    @login_required
    def post(self):
        news = NewsManager()
        if self.form.validate_on_submit():
            file = self.form.img.data
            self.f_manager.add_img([file])
            res = news.add_new_post(self.form.data, file.filename.lower())
            if res:
                flash('Статься успешно добавлена, спасибо!', category='success')
        else:
            flash('Вы не заполнили все поля', category='danger')
            return make_response(render_template('admin_news.html', form=self.form), 200, HEADERS)

        return redirect(url_for('anews'))


class AGetThere(Resource):
    """
        Обработчик для страницы
            с редактированием страницы с местоположением
    """

    @login_required
    def get(self):
        return make_response(render_template('admin_getthere.html'), 200, HEADERS)


class AFeedBack(Resource):
    """
        Обработчик для страницы
                    со списком отзывов
    """

    @login_required
    def get(self):
        fb = FeedbackManager()
        feedback = fb.get_admin_feedback()
        return make_response(render_template('admin_feedback.html', feedback=feedback), 200, HEADERS)


class ACatalog(Resource):
    """
           Обработчик для страницы
                   для загрузки фотографий
    """

    @login_required
    def get(self, method='show', path=''):
        return make_response(render_template('admin_gallery.html', gallery=FileManager(path)), 200, HEADERS)

    @login_required
    def post(self, method='show', path='', img_name=''):
        f_manager = FileManager(path)

        match method:
            case 'create_img':
                file = request.files.getlist('file')
                if file[0].filename:
                    f_manager.add_img(file)
            case 'create_dir':
                if name := request.form['name']:
                    f_manager.create_dir(name)
                path = f_manager.inf["path"]
            case 'delete_img':
                f_manager.del_img(img_name)
            case 'delete_dir':
                f_manager.del_dir()
                path = f_manager.inf["path"]

        return make_response(render_template('admin_gallery.html', gallery=FileManager(path)), 200, HEADERS)


class ADeleteFeedBack(Resource):
    """
           Обработчик для
                   удаления фидбека
    """

    @login_required
    def get(self, id=''):
        fb = FeedbackManager()
        fb.delete_feedback(id)
        return redirect(url_for('afeedback'))


class AShowNews(Resource):
    """
           Обработчик страницы
                   редактирования новости фотографий
    """

    def __init__(self):
        self.news = NewsManager()
        self.form = NewsForm()
        self.path = 'posts'

    @login_required
    def get(self, url=''):
        news_page = self.news.show_news(url)
        return make_response(render_template('admin_post.html', news=news_page, form=self.form), 200, HEADERS)

    @login_required
    def post(self, url=''):
        file = self.form.img.data
        img = self.news.show_news(url).img
        if file:
            f_manager = FileManager(self.path)
            f_manager.del_img(img)
            f_manager.add_img([file])
            res = self.news.update_news(url, request.form['title_new'], request.form['text_new'], file.filename.lower())
            if not res:
                flash('Ошибка обновления поста')
        else:
            res = self.news.update_news(url, request.form['title_new'], request.form['text_new'], img)
            if not res:
                flash('Ошибка обновления поста')
        return redirect(f'/admin/news/{url}')


class ANewsAnonnce(Resource):
    """
           Обработчик страницы
                   со всеми новостями
    """

    @login_required
    def get(self):
        news = NewsManager()
        all_news = news.get_news_anonnce()
        return make_response(render_template('admin_list_news.html', news=all_news), 200, HEADERS)


class ADeleteNews(Resource):
    """
           Обработчик для
                   удаления новости
    """

    @login_required
    def get(self, url=''):
        news = NewsManager()
        img = news.show_news(url).img
        path = 'posts'
        f_manager = FileManager(path)
        f_manager.del_img(img)
        news.delete_news(url)
        flash(f'Новость успешно удалена!')
        return redirect(url_for('anewsanonnce'))


class AMembersAdd(Resource):
    """
        Обработчик для страницы
            с добавлением участников
    """

    def __init__(self):
        self.path = 'members'
        self.form = MembersForm()
        self.f_manager = FileManager(self.path)

    @login_required
    def get(self):
        return make_response(render_template('admin_members.html', form=self.form), 200, HEADERS)

    @login_required
    def post(self):
        mb = MembersManager()
        if self.form.validate_on_submit():
            file = self.form.img.data
            self.f_manager.add_img([file])
            res = mb.add_new_members(self.form.data, file.filename.lower())
            if res:
                flash('Участник успешно добавлен, спасибо!', category='success')
        else:
            flash('Вы указали неподходящую информацию', category='danger')
            return make_response(render_template('admin_members.html', form=self.form), 200, HEADERS)

        return redirect(url_for('amembersadd'))


class AShowMember(Resource):
    """
           Обработчик страницы
                   редактирования конкретного участника
    """

    def __init__(self):
        self.mb = MembersManager()
        self.form = MembersForm()
        self.path = 'members'

    @login_required
    def get(self, pavilion=''):
        member_page = self.mb.show_member(pavilion)
        return make_response(render_template('member_page.html', members=member_page, form=self.form), 200, HEADERS)

    @login_required
    def post(self, pavilion=''):
        file = self.form.img.data
        img = self.mb.show_member(pavilion).img
        if file:
            f_manager = FileManager(self.path)
            f_manager.del_img(img)
            f_manager.add_img([file])
            res = self.mb.update_member(pavilion, request.form['title_new'], request.form['text_new'],
                                        file.filename.lower())
            if not res:
                flash('Ошибка обновления поста')
        else:
            res = self.mb.update_member(pavilion, request.form['title_new'], request.form['text_new'], img)
            if not res:
                flash('Ошибка обновления поста')
        return redirect(f'/admin/members/{pavilion}')


class AMembersAnonnce(Resource):
    """
           Обработчик страницы
                   со всеми участниками
    """

    @login_required
    def get(self):
        mb = MembersManager()
        all_members = mb.get_members_anonnce()
        return make_response(render_template('admin_list_members.html', members=all_members), 200, HEADERS)


class ADeleteMembers(Resource):
    """
           Обработчик для
                   удаления участника
    """

    @login_required
    def get(self, pavilion=''):
        mb = MembersManager()
        img = mb.show_member(pavilion).img
        path = 'members'
        f_manager = FileManager(path)
        f_manager.del_img(img)
        mb.delete_members(pavilion)
        flash(f'Участник успешно удален!')
        return redirect(url_for('amembersanonnce'))

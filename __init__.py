from flask import Flask
from flask_restful import Api
from config import Config
from flask_login import LoginManager
from models.authorization import UserLogin
from controllers.main_controller import Index, News, GetThere, Feedback, LoginPage, Gallery, ImageViewer, \
    ShowNews, Members, ShowMembers
from controllers.admin_controller import AIndex, ANews, AGetThere, AFeedBack, ACatalog, ADeleteFeedBack, \
    AShowNews, ANewsAnonnce, ADeleteNews, AMembersAdd, AShowMember, AMembersAnonnce, ADeleteMembers

app = Flask(__name__, template_folder='views')
api = Api(app)

app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = "loginpage"
login_manager.login_message = "Авторизуйтесь для просмотра этой страницы"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)

# user pages

api.add_resource(Index, '/', '/home', '/index')
api.add_resource(News, '/news')
api.add_resource(ShowNews, '/news/<url>')
api.add_resource(Members, '/members')
api.add_resource(ShowMembers, '/members/<pavilion>')
api.add_resource(GetThere, '/getthere')
api.add_resource(Feedback, '/feedback')
api.add_resource(Gallery, '/gallery/<path>')
api.add_resource(ImageViewer, '/image/<path>/<file>')
api.add_resource(LoginPage, '/login')

# admin pages

api.add_resource(AIndex, '/admin', '/admin/')
api.add_resource(AMembersAdd, '/admin/addmembers')
api.add_resource(AShowMember, '/admin/members/<pavilion>')
api.add_resource(ADeleteMembers, '/admin/members/delete/<pavilion>')
api.add_resource(AMembersAnonnce, '/admin/members')
api.add_resource(ANews, '/admin/news')
api.add_resource(ANewsAnonnce, '/admin/listnews')
api.add_resource(AShowNews, '/admin/news/<url>')
api.add_resource(ADeleteNews, '/admin/news/delete/<url>')
api.add_resource(AGetThere, '/admin/getthere')
api.add_resource(AFeedBack, '/admin/feedback')
api.add_resource(ACatalog, '/admin/catalog/<method>', '/admin/catalog/<method>/<path>',
                 '/admin/catalog/<method>/<path>/<img_name>')
api.add_resource(ADeleteFeedBack, '/admin/feedback/delete/<id>')

if __name__ == '__main__':
    app.run(debug=True)

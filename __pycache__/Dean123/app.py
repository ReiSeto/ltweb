import os.path

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from view.base_model_view import BaseModelView

USERNAME_DB = 'root'
PASSWORD_DB = '123456'
NAME_DB = 'dean'
IP_DB = 'localhost'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = \
    str.format(f"mysql+pymysql://{USERNAME_DB}:{PASSWORD_DB}@{IP_DB}/{NAME_DB}?charset=utf8mb4")
app.config['SECRET_KEY'] = 'lsdhflkjslkfjjeijfwef'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class HomeView(AdminIndexView):
    def is_visible(self):
        return not current_user.is_authenticated

    @expose('/')
    def index(self):
        return self.render('html/login.html')


admin = Admin(
    app
    # index_view=HomeView()
    # url='/admin'
)


class AdminModel(UserMixin, db.Model):
    __tablename__ = 'adminn'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.DateTime)
    status = db.Column(db.String(50), default=None)

    def get_id(self):
        return self.admin_id

    def __str__(self):
        return self.name


class CateBlogModel(db.Model):
    __tablename__ = 'cateblog'

    cateblog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

#
# class BlogModel(db.Model):
#     __tablename__ = 'blog'
#
#     blog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     admin_id = db.Column(db.Integer, ForeignKey('adminn.admin_id'), nullable=False)
#     title = db.Column(db.String(50), nullable=False)
#     datecre = db.Column(db.TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)
#     image = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     cateblog_id = db.Column(db.Integer, ForeignKey('cateblog.cateblog_id'), nullable=False)
#
#     # Define relationships
#     admin = relationship('AdminModel', backref='blogs')
#     category = relationship('CateBlog', backref='blogs')


# class CommentModel(db.Model):
#     __tablename__ = 'comment'
#
#     cmt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     content = db.Column(db.String(200), nullable=False)
#     datecre = db.Column(db.TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog.blog_id', ondelete='CASCADE'))
#
#     # Define relationship
#     blog = relationship('Blog', backref='comments')


class UserContactModel(db.Model):
    __tablename__ = 'user_contact'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer)
    datecre = db.Column(db.TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)


class CateProjectModel(db.Model):
    __tablename__ = 'cateproject'

    cateproj_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)


class ProjectModel(db.Model):
    __tablename__ = 'project'

    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    subTitle = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    datecre = db.Column(db.TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)
    admin_id = db.Column(db.Integer, ForeignKey('adminn.admin_id'), nullable=False)
    photoURL = db.Column(db.String(100), nullable=False)
    cateproj_id = db.Column(db.Integer, ForeignKey('cateproject.cateproj_id'), nullable=False)



@login_manager.user_loader
def load_user(admin_id):
    return AdminModel.query.get(int(admin_id))


# class MyModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#     def inaccessible_callback(self, name, **kwargs):
#         # Redirect to login page if user is not logged in
#         return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('html/index.html')


# @app.route('/admin', methods=['GET', 'POST'])
# def login_admin():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = AdminModel.query.filter_by(username=username).first()
#         if user and password == user.password:
#             login_user(user)
#     return redirect('/admin')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


class CateBlogView(BaseModelView):
    pass


class UserContactView(BaseModelView):
    pass


class CateProjectView(BaseModelView):
    pass


class ProjectView(BaseModelView):
    column_list = ['project_id', 'title', 'subTitle', 'content', 'datecre', 'admin_id', 'photoURL', 'cateproj_id']

    # Add the custom view to the menu
    def is_visible(self):
        return True


# Other routes and functions...
admin.add_view(BaseModelView(AdminModel, db.session, name="Quản trị viên"))
admin.add_view(CateBlogView(CateBlogModel, db.session, name="Loại blog"))
# admin.add_view(BaseModelView(BlogModel, db.session, name="Blog"))
# admin.add_view(BaseModelView(CommentModel, db.session, name="Bình luận"))
admin.add_view(CateProjectView(CateProjectModel, db.session, name="Loại Project"))
admin.add_view(ProjectView(ProjectModel, db.session, name="Project"))
admin.add_view(UserContactView(UserContactModel, db.session, name="Thông tin liên hệ"))
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
import hashlib
import os.path

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_admin.form import rules
from wtforms import IntegerField
from wtforms.validators import DataRequired

from view.Admin.account_view import AccountView
from view.base_model_view import BaseModelView

USERNAME_DB = 'root'
PASSWORD_DB = 'phamtranyennhi16'
NAME_DB = 'dean123'
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
        return self.render('admin/home_page.html', username=current_user)


admin = Admin(app=app, name="GO", template_mode="bootstrap4",
              index_view=HomeView(name='Trang chủ'))


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

    def set_password(self, password):
        hashed_password = hashlib.md5(password.encode('utf8')).hexdigest()
        print(f"Setting password for {self.username}: {hashed_password}")
        self.password = hashed_password


class CateBlogModel(db.Model):
    __tablename__ = 'cateblog'

    cateblog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)


class BlogModel(db.Model):
    __tablename__ = 'blog'

    blog_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(50), nullable=False)
    datecre = db.Column(db.TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)
    image = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cateblog_id = db.Column(db.Integer, nullable=False)
    link = db.Column(db.Text)

    # # Define relationships
    # admin = relationship('AdminModel', backref='blogs')
    # category = relationship('CateBlog', backref='blogs')


class CommentModel(db.Model):
    __tablename__ = 'comment'

    cmt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    datecre = db.Column(db.TIMESTAMP, server_default='CURRENT_TIMESTAMP', nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.blog_id', ondelete='CASCADE'))
#
#     # Define relationship
#     blog = relationship('Blog', backref='comments')


class UserContactModel(db.Model):
    __tablename__ = 'user_contact'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)


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
    admin_id = db.Column(db.Integer, nullable=False)
    photoURL = db.Column(db.String(100), nullable=False)
    cateproj_id = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(admin_id):
    return AdminModel.query.get(int(admin_id))


@app.route('/index')
def index():
    return render_template('html/index.html')


def get_account(username=None, password=None):
    if username and password:
        return AdminModel.query.filter(AdminModel.username.__eq__(username),
                                         AdminModel.password.__eq__(
                                             hashlib.md5(password.encode('utf8')).hexdigest())).first()


@app.route("/admin", methods=['POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            account = get_account(username, password)
        else:
            account = None
        if account:
            login_user(user=account)
    return redirect('/admin')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_admin'))


class HomeView(AdminIndexView):
    def is_visible(self):
        return current_user.is_authenticated

    @expose('/')
    def index(self):
        return self.render('admin/home_page.html')


class CateBlogView(BaseModelView):
    can_edit = False
    can_create = False
    can_delete = False

    def is_visible(self):
        return True


class UserContactView(BaseModelView):
    can_delete = True
    can_create = False
    can_edit = False

    def is_visible(self):
        return True


class CateProjectView(BaseModelView):
    def is_visible(self):
        return True


class CommentView(BaseModelView):
    column_list = ['cmt_id', 'username', 'email', 'content', 'datecre', 'blog_id',]
    can_edit = False;

    def is_visible(self):
        return True


class ProjectView(BaseModelView):
    form_args = {
        'admin_id': {
            'label': 'Admin ID',
            'validators': [DataRequired()]
        },
        'cateproj_id': {
            'label': 'Cateproj ID',
            'validators': [DataRequired()]
        }
    }

    form_extra_fields = {
        'admin_id': IntegerField('Admin ID', [DataRequired()]),
        'cateproj_id': IntegerField('Cateproj ID', [DataRequired()])
    }
    form_rules = [
        rules.FieldSet(('title', 'subTitle', 'content', 'datecre', 'admin_id', 'photoURL', 'cateproj_id'), 'Project Info'),
    ]


class BlogView(BaseModelView):
    column_list = ['blog_id','admin_id','title', 'datecre', 'image', 'content', 'cateblog_id','link' ]
    column_searchable_list = ['title']

    def is_visible(self):
        return True

    # form_rules = [
    #     rules.FieldSet(('title', 'datecre', 'image', 'content', 'link','admin_id'), 'Thông tin blog'),
    #     # rules.FieldSet(('admin_id', 'cateblog_id'), 'Các thông tin khác')
    # ]


@app.route('/blog')
def blog():
    blog_posts = BlogModel.query.all()

    return render_template('html/blog.html', blog_posts=blog_posts)


@app.route('/project')
def project():
    projects = ProjectModel.query.all()

    return render_template('html/project.html', projects=projects)


@app.route('/')
def home():
    return render_template('html/home.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['newsletter1']
        new_usercontact = UserContactModel(email=email)

        try:
            db.session.add(new_usercontact)
            db.session.commit()
        except:
            db.session.rollback()
        return render_template('html/subscribe.html')


def initAdmin():
    admin.add_view(AccountView(AdminModel, db.session, name="Quản trị viên"))
    admin.add_view(CateBlogView(CateBlogModel, db.session, name="Loại blog"))
    admin.add_view(BlogView(BlogModel, db.session, name="Blog"))
    admin.add_view(CommentView(CommentModel, db.session, name="Bình luận"))
    admin.add_view(CateProjectView(CateProjectModel, db.session, name="Loại Project"))
    admin.add_view(ProjectView(ProjectModel, db.session, name="Project"))
    admin.add_view(UserContactView(UserContactModel, db.session, name="Thông tin liên hệ"))


if __name__ == '__main__':
    initAdmin()
    app.run(port=5002, debug=True)
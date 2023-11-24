# from flask import Flask
# from flask_admin import Admin
# from flask_admin.model import BaseModelView
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask import Flask, render_template
#
# from app import CateBlogView, BlogView, CommentView, CateProjectView, ProjectView, UserContactView, AdminModel, \
#     CateBlogModel, BlogModel, CommentModel, CateProjectModel, ProjectModel, UserContactModel, HomeView
#
# app = Flask(__name__)
#
# # mysql account
# USERNAME_DB = 'root'
# PASSWORD_DB = 'phamtranyennhi16'
# NAME_DB = 'dean'
# IP_DB = 'localhost'
#
# app.config["SQLALCHEMY_DATABASE_URI"] = \
#     str.format(f"mysql+pymysql://{USERNAME_DB}:{PASSWORD_DB}@{IP_DB}/{NAME_DB}?charset=utf8mb4")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["FLASK_ADMIN_FLUID_LAYOUT"] = True
# # app.config["SQLALCHEMY_ECHO"] = True
# app.secret_key = b'21137afa59a4dd08b708dcf106c724f9'
# db = SQLAlchemy(app=app)
#
# login = LoginManager(app=app)
#
#
# @app.route('/')
# def index():  # put application's code here
#     return render_template('client/index.html')
#
#
# @app.route('/donate')
# def donate():  # put application's code here
#     return render_template('client/donate.html')
#
#
# @app.route('/aboutus')
# def aboutus():  # put application's code here
#     return render_template('client/aboutus.html')
#
#
# @app.route('/contact')
# def contact():  # put application's code here
#     return render_template('client/contact_index.html')
#
#
# @app.route('/blog')
# def blog():  # put application's code here
#     return render_template('client/ex.html')
#
#
# def initTables():
#     try:
#         db.create_all()
#     except:
#         db.session.rollback()
#
#
# def initAdmin():
#     admin.add_view(BaseModelView(AdminModel, db.session, name="Quản trị viên"))
#     admin.add_view(CateBlogView(CateBlogModel, db.session, name="Loại blog"))
#     admin.add_view(BlogView(BlogModel, db.session, name="Blog"))
#     admin.add_view(CommentView(CommentModel, db.session, name="Bình luận"))
#     admin.add_view(CateProjectView(CateProjectModel, db.session, name="Loại Project"))
#     admin.add_view(ProjectView(ProjectModel, db.session, name="Project"))
#     admin.add_view(UserContactView(UserContactModel, db.session, name="Thông tin liên hệ"))
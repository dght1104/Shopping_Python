from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from os import path
from flask_login import LoginManager
from flask_mail import Message, Mail
from flask_migrate import Migrate  # ✅ Migrate được import

# Khởi tạo đối tượng toàn cục
db = SQLAlchemy()
migrate = Migrate()  # ✅ Đăng ký Flask-Migrate toàn cục

# Thông tin cấu hình kết nối
server = 'DGHT1104'
database = 'PeacefulPagesSanctuary'
driver = 'ODBC Driver 17 for SQL Server'
DB_NAME = 'PeacefulPagesSanctuary'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'giahan'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mssql+pyodbc://@{server}/{database}?driver={driver.replace(" ", "+")}&Trusted_Connection=yes'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo database và migrate
    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Kết nối migrate với app và db

    from .view import views
    from .auth import auth
    from .admin import admin 
    from .models import Customer

    # create_database(app)

    # Cấu hình Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'trandonggiahan2003@gmail.com'
    app.config['MAIL_PASSWORD'] = 'yjqulsrnrzgwedaq'
    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
    mail = Mail(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def loader_user(cus_id):
        return Customer.query.get(int(cus_id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.mail = mail

    return app

def create_database(app):
    # ⚠️ Kiểm tra file tồn tại không phù hợp với SQL Server
    with app.app_context():
        db.create_all()
        print('Created Database!')

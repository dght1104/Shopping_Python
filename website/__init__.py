from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
# Thông tin cấu hình kết nối
server = 'DGHT1104'  # Tên server
database = 'db_shop'  # Tên cơ sở dữ liệu
driver = 'ODBC Driver 17 for SQL Server'

DB_NAME='db_shop'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='giahan'
    app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://@{server}/{database}?driver={driver.replace(" ", "+")}&Trusted_Connection=yes')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Khởi tạo SQLAlchemy
    db.init_app(app)

    from .view import views
    from .auth import auth
    
    from .models import Customer
    create_database(app)

    login_manager=LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def loader_user(cus_id):
        return Customer.query.get(int(cus_id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()  # Tạo các bảng trong database
            print('Created Database!')
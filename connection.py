from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Thông tin cấu hình kết nối
server = 'DGHT1104'  # Tên server
database = 'PeacefulPagesSanctuary'  # Tên cơ sở dữ liệu
driver = 'ODBC Driver 17 for SQL Server'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mssql+pyodbc://@{server}/{database}?driver={driver.replace(" ", "+")}&Trusted_Connection=yes'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Khởi tạo SQLAlchemy
db = SQLAlchemy(app)

# Kiểm tra kết nối trực tiếp với pyodbc (nếu cần)
try:
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes'
    )
    print("Kết nối thành công bằng pyodbc (Windows Authentication)!")
    conn.close()
except Exception as e:
    print("Lỗi kết nối pyodbc:", e)

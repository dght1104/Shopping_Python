# from flask import Flask, redirect , url_for, render_template, request, session, flash
# from flask_sqlalchemy import SQLAlchemy
# import pyodbc

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# # Thông tin cấu hình kết nối
# server = 'DGHT1104'  # Tên server
# database = 'db_shop'  # Tên cơ sở dữ liệu
# driver = 'ODBC Driver 17 for SQL Server'

# # Chuỗi kết nối sử dụng SQLAlchemy với pyodbc (Windows Authentication)
# # app.config['SQLALCHEMY_DATABASE_URI'] = (
# #     f'mssql+pyodbc://@{server}/{database}?driver={driver.replace(" ", "+")}&Trusted_Connection=yes'
# # )
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # # Khởi tạo SQLAlchemy
# # db = SQLAlchemy(app)

# # # Kiểm tra kết nối trực tiếp với pyodbc (nếu cần)
# # try:
# #     conn = pyodbc.connect(
# #         f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes'
# #     )
# #     print("Kết nối thành công bằng pyodbc (Windows Authentication)!")
# #     conn.close()
# # except Exception as e:
# #     print("Lỗi kết nối pyodbc:", e)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/login', methods=["POST","GET"])
# def login():
#     if request.method=="POST":
#         user_name =request.form["name"]
#         if user_name :
#             session["user"]=user_name
#             return redirect(url_for("name_user",name=user_name))
#     if  "user" in session:
#         name = session["user"]
#         return f"helo {name}"
#     return render_template("login.html")

# @app.route('/user/')
# def name_user():
#     if "user" in session:
#         name = session["user"]
#         return f"helo {name}"
#     else:
#         return redirect(url_for("login"))

# @app.route('/logout', methods=["POST","GET"])
# def logout():
#     session.pop("user",None)
#     return render_template("login.html")

# if __name__ == "__main__":
#     app.run(debug=True)
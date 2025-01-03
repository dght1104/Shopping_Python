from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Customer
from flask_sqlalchemy import SQLAlchemy
from . import db
auth = Blueprint('auth', __name__)

@auth.route('/login',methods=["POST","GET"])
def login():
    data=request.form
    print(data)
    return render_template('login.html')
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
    
@auth.route('/logout')
def logout():
    
    return "Logout"

@auth.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        user=Customer.query.filter.by(cus_username=user_name).first()
        if user:
            flash("Tên đăng nhập đã tồn tại")
        elif len(user_name) < 6:
            flash("Tên đăng nhập phải dài hơn 6", category='error') 
        elif len(password) < 6:
            flash("Mật khẩu phải dài hơn 6 kí tự", category='error') 
        elif password!= password1:
            flash("Mật khẩu không trùng khớp", category='error') 
        else:
            new_user=Customer(cus_username=user_name, cus_password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Tạo tài khoản thành công", category='success') 
            return redirect(url_for('views.home'))
    return render_template('signup.html')
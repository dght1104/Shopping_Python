from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Customer
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
auth = Blueprint('auth', __name__)

@auth.route('/login',methods=["POST","GET"])
def login():
    user = None
    if request.method == "POST":
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        print(f"Username: {user_name}, Password: {password}")  # In ra giá trị của user_name và password
        user = Customer.query.filter_by(cus_username=user_name).first()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user:
            print(f"input password: {hashed_password}")
            print(f"Stored password: {user.cus_password}")  # In ra mật khẩu lưu trong DB
            db_password = user.cus_password.strip() 
            if db_password == hashed_password:
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Sai mật khẩu", category='error')
        else:
            flash("Tên đăng nhập không tồn tại", category='error')
    signup_url = url_for('auth.signup')
    register_message = f'Bạn chưa có tài khoản, hãy <a href="{signup_url}">đăng ký ngay</a>!'
    return render_template('login.html',user=user, register_message=register_message)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        user=Customer.query.filter_by(cus_username=user_name).first()
        if user:
            flash("Tên đăng nhập đã tồn tại", category='error')
        elif len(user_name) < 6:
            flash("Tên đăng nhập phải dài hơn 6", category='error') 
        elif len(password) < 6:
            flash("Mật khẩu phải dài hơn 6 kí tự", category='error') 
        elif password!= password1:
            flash("Mật khẩu không trùng khớp", category='error') 
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            new_user=Customer(cus_username=user_name, cus_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Tạo tài khoản thành công", category='success') 
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template('signup.html',  user=current_user)
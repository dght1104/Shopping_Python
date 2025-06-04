from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import Customer
from . import db
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
from flask_mail import Message, Mail
import secrets
import random, time
from flask import current_app

otp_store = {}  
auth = Blueprint('auth', __name__)
mail = Mail()

# Lưu token xác thực tạm thời (thường bạn nên lưu database)
email_verification_tokens = {}

@auth.route('/signup', methods=["POST","GET"])
def signup():
    if request.method == "POST":
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('password1')

        user = Customer.query.filter_by(cus_username=user_name).first()
        if user:
            flash("Tên đăng nhập đã tồn tại", category='error')
        elif len(user_name) < 6:
            flash("Tên đăng nhập phải dài hơn 6", category='error') 
        elif len(password) < 6:
            flash("Mật khẩu phải dài hơn 6 kí tự", category='error') 
        elif password != password1:
            flash("Mật khẩu không trùng khớp", category='error') 
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            new_user = Customer(cus_username=user_name, cus_email=email, cus_password=hashed_password, is_verified=False)
            db.session.add(new_user)
            db.session.commit()

             # Gửi mã OTP
            otp_code = str(random.randint(100000, 999999))
            expire_time = time.time() + 300  # Hết hạn sau 5 phút
            otp_store[user_name] = (otp_code, expire_time)

            # Gửi mail có mã OTP
            send_otp_email(email, otp_code)

            flash("Tạo tài khoản thành công! Vui lòng kiểm tra email để nhập mã OTP.", category='success')
            return redirect(url_for('auth.verify_otp', username=user_name))
        
    return render_template('auth/signup.html', user=current_user)

@auth.route('/verify_otp/<username>', methods=['GET', 'POST'])
def verify_otp(username):
    if request.method== 'POST':
        username_form= request.form.get('username')
        otp_input= request.form.get('otp_verify')

        if not username_form or username_form not in otp_store:
            flash('user hoặc otp k tồn tại')
            return redirect(url_for('auth.signup'))
        
        otp_code, expire_time= otp_store.get(username_form)

        if time.time() > expire_time:
            flash('mã otp hết hạn', 'error')
            otp_store.pop(username_form, None)
            return redirect(url_for('auth.signup'))
        
        if otp_input == otp_code:
            user = Customer.query.filter_by(cus_username=username_form).first()
            if user:
                user.is_verified= True
                db.session.commit()
                otp_store.pop(username_form, None)
                flash('xác thực thành công', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('người dùng không tồn tại', 'error')
        else:
            flash('Mã ko chính xác','error')
    return render_template('auth/verify_otp.html', username=username)

@auth.route('/login', methods=["POST","GET"])
def login():
    user = None
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print("POST received:", email, password)
        
        user = Customer.query.filter_by(cus_email=email).first()
        if not user:
            flash("Tên đăng nhập không tồn tại", category='error')
            print("User not found")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest().upper()
            db_password = user.cus_password.strip()
            print(f"DB pass: {db_password}, hashed input: {hashed_password}")
            if db_password == hashed_password:
                login_user(user, remember=True)
                print("Login successful")
                return redirect(url_for('views.home'))
            else:
                flash("Sai mật khẩu", category='error')
                print("Wrong password")
    return render_template('auth/login.html', user=user)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

def send_otp_email(to_email, otp_code):
    msg= Message(
        subject="Xác thực tài khoản",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to_email],
        body=f"Mã xác thực: {otp_code}"
    )

    try:
       current_app.mail.send(msg)
    except Exception as e:
        print("gửi thất bạ: ". str(e))
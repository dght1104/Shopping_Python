from flask import Blueprint, render_template, request, flash

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
        if len(user_name) < 6:
            flash("Tên đăng nhập phải dài hơn 6", category='error') 
        elif len(password) < 8:
            flash("Mật khẩu phải dài hơn 8 kí tự", category='error') 
        elif password!= password1:
            flash("Mật khẩu không trùng khớp", category='error') 
        else:
            flash("Tạo tài khoản thành công", category='success') 
    return render_template('signup.html')
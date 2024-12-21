from flask import Flask, redirect , url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://username:password@hostname/database_name?driver=ODBC+Driver+17+for+SQL+Server'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Tắt theo dõi thay đổi

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method=="POST":
        user_name =request.form["name"]
        if user_name :
            session["user"]=user_name
            return redirect(url_for("name_user",name=user_name))
    if  "user" in session:
        name = session["user"]
        return f"helo {name}"
    return render_template("login.html")

@app.route('/user/')
def name_user():
    if "user" in session:
        name = session["user"]
        return f"helo {name}"
    else:
        return redirect(url_for("login"))

@app.route('/logout', methods=["POST","GET"])
def logout():
    session.pop("user",None)
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
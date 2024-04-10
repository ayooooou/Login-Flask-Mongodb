from flask import Flask, request, render_template,redirect,url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config["MONGO_URI"] = f"mongodb+srv://yoyokuo1129:{os.getenv('config_MONGO_URI')}@cluster0.zw1xmlv.mongodb.net/user"
app.secret_key = os.getenv('app_secret_key')
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin):
    pass

@app.route("/")
def home_page():
    return render_template("home.html",current_user=current_user)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    error_message = ""
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        existing_email = mongo.db.user.find_one({'email': email})
        existing_username = mongo.db.user.find_one({'username': username})
        if existing_email:
            error_message += "\nEmail already exists!"
        if existing_username:
            error_message += "\nUsername already exists!"
        if not existing_email and not existing_username:
            user = {'email': email, 'username': username, 'password': password}
            mongo.db.user.insert_one(user)
            return redirect(url_for('login_page'))
    return render_template("register.html",error_message=error_message,current_user=current_user)

@app.route("/login", methods=['GET','POST'])
def login_page():
    error_message = ""
    if request.method == 'POST':
        if current_user.is_active: 
            return 'has logined'
        username = request.form['username']
        password = request.form['password']
        user_find = mongo.db.user.find_one({'username': username})
        if user_find and user_find['password']==password:
            user = User()  #  實作User類別
            user.id = username #為了讓 Flask-Login 知道哪個用戶已經登入
            login_user(user)   
            return render_template("home.html",current_user=current_user)
        elif user_find:
            error_message = '\nWrong password'
        else:
            error_message = "\nUnknown username"
        return render_template("login.html",error_message=error_message,current_user=current_user)
    return render_template("login.html")


@login_manager.user_loader  
def user_loader(username):  
    user = User()  
    user.id = username
    return user 

@app.route('/logout')  
def logout_page():  
    if current_user.is_active: 
        logout_user()  
        return 'Logged out'
    else:
        return "you aren't login"
    

@app.route('/protected')  
@login_required  #只能在用戶登錄後訪問
def protected_page():  
    #  current_user取得登錄狀態
    if current_user.is_active:  
        return 'Logged in as: ' + current_user.id + 'Login is_active:True'

if __name__ == '__main__':
    app.run(debug=True,port=8000)
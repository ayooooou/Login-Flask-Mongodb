from flask import Flask, request, render_template,redirect,url_for,session
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config["MONGO_URI"] = f"mongodb+srv://yoyokuo1129:{os.getenv('config_MONGO_URI')}@cluster0.zw1xmlv.mongodb.net/user"
app.secret_key = os.getenv('app_secret_key')
mongo = PyMongo(app)
# app.config['SESSION_TYPE'] = 'mongodb'
# app.config['SESSION_MONGODB'] = f"mongodb+srv://yoyokuo1129:{os.getenv('config_MONGO_URI')}@cluster0.zw1xmlv.mongodb.net/"
# app.config['SESSION_MONGODB_DB'] = "session"
# app.config['SESSION_MONGODB_COLLECT'] = "session"
#session = Session(app)

@app.route("/")
def home_page():
    return render_template("home.html")

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
    return render_template("register.html",error_message=error_message)

@app.route("/login", methods=['GET','POST'])
def login_page():
    error_message = ""
    if request.method == 'POST':
        if session.get('state') == "login" : 
            return 'has logined'
        username = request.form['username']
        password = request.form['password']
        user_find = mongo.db.user.find_one({'username': username})
        if user_find and user_find['password']==password:
            session['state'] = "login"
            session['username'] = username
            return render_template("home.html")
        elif user_find:
            error_message = '\nWrong password'
        else:
            error_message = "\nUnknown username"
        return render_template("login.html",error_message=error_message)
    return render_template("login.html")

@app.route('/logout')  
def logout_page():  
    if session.get('state') == "login": 
        session['state'] = "logout"
        session.pop('username',None) 
        return 'Logged out'
    else:
        return "you aren't login"
    
@app.route('/protected')  
def protected_page():  
    if 'username' in session:  
        return 'Logged in as: ' + session.get('username') + ' Your password is '+ mongo.db.user.find_one({'username':session.get('username')})['password']

if __name__ == '__main__':
    app.run(debug=True,port=8000)
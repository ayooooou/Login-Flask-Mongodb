from flask import Flask, request, render_template,redirect,url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
app.secret_key = 'hello,wood'
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def home_page():
    return render_template("home.html",)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        user = {'email': email, 'username': username, 'password': password}
        mongo.db.user.insert_one(user)
        return redirect(url_for('home_page'))
    return render_template("register.html")

@app.route("/login", methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_find = mongo.db.user.find_one({'username': username})
        if user_find and user_find['password']==password:
            #  實作User類別  
            user = User()  
            #  設置id就是email  
            user.id = username
            #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
            login_user(user)  
            return redirect(url_for('home_page'))
        return '登入失敗'
    return render_template("login.html")


@app.route('/submit/login', methods=['POST'])
def submit_login():
    username = request.form['username']
    password = request.form['password']
    user_find = mongo.db.user.find_one({'username': username})
    if user_find and user_find['password']==password:
        #  實作User類別  
        user = User()  
        #  設置id就是email  
        user.id = username
        #  這邊，透過login_user來記錄user_id，如下了解程式碼的login_user說明。  
        login_user(user)  
        return redirect(url_for('home_page'))  
    return '登入失敗'  

class User(UserMixin):
    pass

@login_manager.user_loader  
def user_loader(username):  
    user = User()  
    user.id = username
    return user 

@app.route('/logout')  
def logout():  
    logout_user()  
    return 'Logged out'

@app.route('/protected')  
@login_required  
def protected():  
    """  
 在login_user(user)之後我們就可以透過current_user.id來取得用戶的相關資訊了  
 """   
    #  current_user確實的取得了登錄狀態
    if current_user.is_active:  
        return 'Logged in as: ' + current_user.id + 'Login is_active:True'

if __name__ == '__main__':
    app.run(debug=True,port=8000)
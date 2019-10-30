import os
import sys
import datetime
import functools
from sqlalchemy import Column, Integer, String, DateTime
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, UserMixin, LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('chat_history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
app.config['SECRET_KEY'] = '.}kp4Gj7egnX-~,;ABEU'
#app.config['SERVER_NAME'] = # NAME
#app.config['SERVER_PORT'] = # Port
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120), unique=True)
    password = Column(String(120))

    def __init__(self, username):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

class Message(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(Integer)
    reciep = Column(Integer)
    text = Column(String(10000))
    timestamp = Column(DateTime)

    def __init__(self, author, reciep, text):
        self.author = author
        self.reciep = reciep
        self.text = text
        self.timestamp = datetime.datetime.now()

def print_err(s):
    print(s, file=sys.stderr)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('include/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('include/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('include/fonts', path)

def messages_compare(x, y):
    if x.timestamp > y.timestamp:
        return 1
    elif x.timestamp < y.timestamp:
        return -1
    else:
        return 0

@app.route('/', methods = ["GET", "POST"])
@login_required
def root():
    if request.method == 'POST':
        text = request.form['message']
        message = Message(current_user.id, current_user.id % 2 + 1, text)
        db.session.add(message)
        db.session.commit()

    messages_author = Message.query.filter_by(author=current_user.id).all()
    messages_reciep = Message.query.filter_by(reciep=current_user.id).all()
    messages = messages_author + messages_reciep
    html_messages = ""
    for m in sorted(messages, key=functools.cmp_to_key(messages_compare)):
        if m.author == current_user.id:
            html_messages += '<p class="author">' + m.text + "</p>"
        else:
            html_messages += '<p class="reciep">' + m.text + "</p>"
    with open('include/html/index.html', 'r', encoding="utf-8") as page:
        data=page.read()
    data = data.replace('%MESSAGE_HISTORY%', html_messages)
    return data

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next = request.args.get('next')
        if next and ('logout' in next):
            next = None
        user = User.query.filter_by(username=username, password=password).first()
        if not (user is None):
            login_user(user, remember=False)
            return redirect('/')
        else:
            return redirect(url_for('login', next=next))
    else:
        with open('include/html/login.html', 'r', encoding="utf-8") as page:
            data=page.read()
        return data

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None
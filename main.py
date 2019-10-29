import os
import sys
from sqlalchemy import Column, Integer, String  
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('chat_history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
#app.config['SERVER_NAME'] = # NAME
#app.config['SERVER_PORT'] = # Port
db = SQLAlchemy(app)

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(120), unique=True)

    def __init__(self, login):
        self.login = login

class Message(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(Integer)
    reciep = Column(Integer)
    text = Column(String(10000))

    def __init__(self, author, reciep, text):
        self.author = author
        self.reciep = reciep
        self.text = text

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

@app.route('/', methods = ["GET", "POST"])
def root():
    if request.method == 'POST':
        text = request.form['message']
        message = Message(1, 1, text)
        db.session.add(message)
        db.session.commit()

    messages = Message.query.all()
    html_messages = ""
    for m in messages:
        if m.author == 1:
            html_messages += '<p class="author">' + m.text + "</p>"
        else:
            html_messages += '<p class="reciep">' + m.text + "</p>"
    with open('include/html/index.html', 'r', encoding="utf-8") as page:
        data=page.read()
    data = data.replace('%MESSAGE_HISTORY%', html_messages)
    return data
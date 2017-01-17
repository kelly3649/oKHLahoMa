from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests as req
from utils import dbUtils as db
import hashlib, os, datetime
import json

app = Flask(__name__)
#creates instance of Flask and passes env variable __name__

app.secret_key = '\x1fBg\x9d\x0cLl\x12\x9aBb\xcd\x17\xb3/\xe4\xca\xf76!\xee\xf2\xc8?\x85\xdb\xd6;[\xae\xfb\xeb'

def HTMLChecker(string):
    return '<' in string or '>' in string

#def fieldChecker(string):
#    return bool(re.search(r'[\\/?%\(\)\'\"\[\]\{\}<>]',string))

def sanitize(string):
    ret = string.replace("'","''")
    return ret

@app.route("/")
def mainpage():
    if 'username' in session:
        page = 1
        post = db.getSomePosts(10, 0)
        return render_template("master.html", posts = post, lastPage = page-1, nextPage = page+1)
    return render_template("logreg.html")

@app.route("/page/<int: pg>"):
def page(pg):
    if 'username' in session:
        post = db.getSomePosts(10, pg)
        return render_template("master.html", posts = post, lastPage = page-1, nextPage = page+1)
    return render_template("logreg.html")

@app.route("/upload")
def upload():
    if 'username' in session:
        image = request.form['image']
        requests.get("")
    return render_template("logreg.html")

@app.route("/checkUser")
def userCheck():
    username = request.args.get("text")

    result = {'result': db.checkUsername(username)}
    
    return json.dumps(result)
        
@app.route("/login", methods=['POST'])
def login():
    if 'username' in session:
        return redirect(url_for("mainpage"))
    username = request.form['username']
    password = hashlib.sha1()
    password.update(request.form['password'])
    password = password.hexdigest()
    if db.checkLogin(username, password):
        session['username'] = username;
        return render_template("master.html")
    else:
        return render_template("logreg.html", loginmessage = "The credentials are wrong. Please try again.")

@app.route("/register", methods=['POST'])
def register():
    if('username' in session):
        return redirect(url_for("mainpage"))
    username = request.form['username']
    password = hashlib.sha1()
    password.update(request.form['password'])
    password = password.hexdigest()
    db.createUser(username,str(password))
    
@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for("mainpage"))
    return redirect(url_for("mainpage"))
      
if __name__ == "__main__":
    app.debug = True
    app.run()

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, requests
from utils import dbUtils as db
import hashlib, os, datetime, time

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
        return redirect(url_for("home"))
    return render_template("logreg.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.sha1()
    password.update(request.form['password'])
    password.hexdigest()
    if checkLogin(username, password):
        session['username'] = username;
        return render.template()

@app.route("/register", methods=['POST'])
def register():
    if('username' in session):
        return redirect(url_for("mainpage"))
    username = request.form['username']
    password = hashlib.sha1()
    password.update(request.form['password'])
    password = password.hexdigest()
    timestamp = int(time.time())
    if db.checkUsername(username):
        message = "Success! Please log in with your credentials."
        db.createUser(username,str(password),timestamp)
        return render_template("logreg.html", error = message)
    else:
        message = "Username exists already. Please choose another username."
        return render_template("logreg.html", error = message)

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        flash("Successfully logged out!")
        return redirect(url_for("mainpage"))
    return redirect(url_for("mainpage"))
      
if __name__ == "__main__":
    app.debug = True
    app.run()

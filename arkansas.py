from flask import Flask, render_template, request, redirect, url_for, session, flash
import utils, sqlite3, re
import hashlib, os

app = Flask(__name__)
#creates instance of Flask and passes env variable __name__

app.secret_key = '\x1fBg\x9d\x0cLl\x12\x9aBb\xcd\x17\xb3/\xe4\xca\xf76!\xee\xf2\xc8?\x85\xdb\xd6;[\xae\xfb\xeb'

def HTMLChecker(string):
    return '<' in string or '>' in string

def fieldChecker(string):
    return bool(re.search(r'[\\/?%\(\)\'\"\[\]\{\}<>]',string))

def sanitize(string):
    ret = string.replace("'","''")
    return ret

@app.route("/")
def mainpage():
    if 'username' in session:
        return redirect(url_for("myFeed"))
    return render_template("login.html")

@app.route("/register", methods=['POST'])
def register():
    if('username' in session):
        return redirect(url_for("mainpage"))
    if(request.form['password'] != request.form['confpass']):
        flash("Passwords must match!")
        return redirect(url_for("mainpage"))
    for key in request.form:
        if fieldChecker(request.form[key]):
            flash("Illegal characters")
            return redirect(url_for("mainpage"))
    success = utils.user_manager.register(request.form['username'],request.form['password'],
                                          request.form['first'],request.form['last'],
                                          request.form['age'],request.form['email'])
    if(success == 2):
        flash("Please fill in all fields!")
        return redirect(url_for("mainpage"))
    if(success == 1):
        flash("Success! : Please Sign In!")
        return redirect(url_for("mainpage"))
    if(success == 0):
        flash("Username already taken!")
        return redirect(url_for("mainpage"))
    if(success == 7):
        flash("Please input an integer value for your age.")
        return redirect(url_for("mainpage"))
    if(success == 3):
        flash("Not enough characters in password.")
    if(success == 4 or success == 9 or success == 10):
        flash("No lowercase letter in password.")
    if(success == 5 or success == 9 or success == 11):
        flash("No uppercase letter in password.")
    if(success == 6 or success == 10 or success == 11):
        flash("No numbers in password.")
    return redirect(url_for("mainpage"))

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

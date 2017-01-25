from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests as req
from utils import dbUtils as db
import hashlib, os, datetime
import json
import random

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

# Returns to login if not logged in, otherwise, returns the first page of pictures. 
@app.route("/")
def mainpage():
    if 'username' in session:
        page = 1
        post = db.getSomePosts(10, 0)
        #print post
        return render_template("feed.html",pagename="Home", canPost = db.canPost(session["username"]), posts = post, lastPage = page-1, nextPage = page+1)
    return render_template("landing.html")

@app.route("/logreg")
def logreg():
    return render_template("logreg.html")

@app.route("/loadMore")
def loadMore():
    pg = request.args.get("page")
    feedOrProfile = request.args.get("type")
    user = request.args.get("user")
    if (feedOrProfile == "feed"):
        posts = db.getSomePosts(10, int(pg))
    else:
        posts = db.getSomePosts(10, int(pg), user)
    return json.dumps(posts)

# Goes to the specified page of posts
@app.route("/page/<int:pg>")
def page(pg):
    if 'username' in session:
        if pg >= 1:
            post = db.getSomePosts(10, pg-1)
        else:
            return redirect(url_for("page", pg=1))
        return render_template("feed.html", pagename="Home", posts = post, lastPage = pg-1, nextPage = pg+1, canPost = db.canPost(session['username']))
    return redirect(url_for("logreg"))

@app.route("/profile/<string:user>")
def profile(user):
    return profilepage(user, 1)

@app.route("/delete", methods=["POST"])
def delete():
    db.deletePost(session["username"], request.form["postid"])
    return redirect(url_for("profile", user=session["username"]))

# Your profile page, or other users profile pages. Will allow you to edit your own.
@app.route("/profile/<string:user>/<int:pg>")
def profilepage(user, pg):
    if 'username' not in session:
        return redirect(url_for("mainpage"))
    else:
        if session['username'] == user:
            condition = True
        else:
            condition = False
        userinfo = db.getUserInfo(user)
        postList = db.getSomePosts(10, pg-1, user)
        return render_template("feed.html", ownprofile = condition, profile = user, posts = postList, info = userinfo, canPost = db.canPost(session["username"]))

@app.route("/myProfile")
def myProfile():
    return profile(session['username'])
        
# Uploads a post with a chosen filter according to the date/time.
@app.route("/upload", methods = ["POST"])
def upload():
    if request.method == "POST":
        if 'username' in session:
            print "KEYS IN REQUEST:"
            for item in request.form:
                print item
            caption = request.form['caption']
            things = { "file" : request.form["sneaky"], "upload_preset" : "bf17cjwp" }
            
            upload = req.post("https://api.cloudinary.com/v1_1/dhan3kbrs/image/upload", data=things)
            response = upload.json()
            photo_name = response["public_id"]
            url = response["secure_url"]
            autofilter = "filter" in request.form
            usespotify = "spotify" in request.form
            imagename = "/" + response["public_id"] #+ "." + response["format"]
            
            print "CREATED POST WITH USERNAME: " + session['username'] + " WITH URL: " + url + " AND WITH CAPTION: " + caption

            if autofilter:
                url = applyFilter(imagename)
                
            if usespotify:
                temp = spotifyGet(caption)
                if temp:
                    caption = temp
            
            if db.canPost(session['username']):
                db.createPost(session['username'], url, caption)
                return redirect(url_for("mainpage"))
            
            else:
                return redirect(url_for("mainpage"))
        return redirect(url_for("mainpage"))

# Ajax extension for checking the user w/o submitting the form.
@app.route("/checkUser")
def userCheck():
    username = request.args.get("text")

    result = {'available': db.checkUsername(username)}
    
    return json.dumps(result)

# Logs the user in successfully if the credentials are correct
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
        return redirect(url_for("mainpage"))
    else:
        return render_template("logreg.html", loginmessage = "The credentials are wrong. Please try again.")

    
# Registers the user. The checking procedure is done in Ajax/JS
@app.route("/register", methods=['POST'])
def register():
    if('username' in session):
        return redirect(url_for("mainpage"))
    username = request.form['username']
    password = hashlib.sha1()
    password.update(request.form['password'])
    password = password.hexdigest()
    db.createUser(username,str(password))
    return render_template("logreg.html", successmsg = "Account successfully created.")

# Logs the user out.
@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        return render_template("logreg.html", successmsg="You have been logged out.")
    return redirect(url_for("mainpage"))

# APPLIES FILTER WITH AN IMAGE NAME
def applyFilter(imagename):
    time = db.getTime()
    improvement = ["e_auto_contrast", "e_improve", "e_auto_color", "e_fill_light"]
    filters = ["e_art:al_dente","e_art:athena","e_art:audrey","e_art:aurora","e_art:daguerre","e_art:eucalyptus","e_art:fes","e_art:frost","e_art:hairspray","e_art:hokusai","e_art:incognito","e_art:linen","e_art:peacock","e_art:primavera","e_art:quartz","e_art:red_rock","e_art:refresh","e_art:sizzle","e_art:sonnet","e_art:ukulele","e_art:zorro"]
    if (random.randint(0,100) < 15):
        option = "e_oil_paint:50/"
    else: option = ""
    effects = ["e_blur:100", "e_sharpen:100", "e_vignette"]
    return "https://res.cloudinary.com/dhan3kbrs/image/upload/" + improvement[time['second'] % 4] + "/" + filters[time['day'] % 21] + "/" + option + effects[time['minute'] % 3] + imagename

# GETS A SPOTIFY SONG FROM A CAPTION
def spotifyGet(songname):
    things = { "q" : songname , "type" : "track"}
    res = req.get("https://api.spotify.com/v1/search", params=things)
    try:
        firstresult = res.json()["tracks"]['items'][0]
    except Exception as e:
        return False
    caption = "<iframe src='https://embed.spotify.com/?uri=%s' frameborder='0' width='100%%' height='80px'></iframe>" % firstresult['uri']
    return caption

if __name__ == "__main__":
    app.debug = True
    app.run()

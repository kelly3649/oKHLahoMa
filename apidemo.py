from flask import Flask, render_template, request
import requests as req

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("nootnoot.html")
    else:
        things = { "file" : request.form["sneaky"], "upload_preset" : "bf17cjwp" }
        uplode = req.post("https://api.cloudinary.com/v1_1/dhan3kbrs/auto/upload", data=things)
        response = uplode.json()
        photo_name = response["public_id"]
        url = response["secure_url"]
        return "<h1>PHOTO ID: %s</h1><img src='%s'></img><h5>%s</h5>" % (photo_name, url, url)

@app.route("/spootify", methods=["POST"])
def spootify():
    things = { "q" : request.form["query"] , "type" : "album,artist,track"}
    res = req.get("https://api.spotify.com/v1/search", params=things)
    dictstr = ""
    for category in ["tracks", "albums", "artists"]:
        if category == "tracks":
            height = '80'
        else:
            height = '380'
        firstresult = res.json()[category]['items'][0]
        dictstr+="<h1>Searched by %s</h1>" % category
        dictstr +=  "<iframe src='https://embed.spotify.com/?uri=%s' frameborder='0' width='300' height='%s'></iframe>" % (firstresult['uri'], height)
        dictstr+="<br>"
    return dictstr

@app.route("/login")
def login():
    return render_template("logreg.html", loginmessage="noo")
    
if __name__ == "__main__":
        app.debug = True
        app.run()

from flask import Flask, render_template, request
import requests as req

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("nootnoot.html")
    else:
        things = { "file" : request.form["sneaky"], "upload_preset" : "bf17cjwp" }
        uplode = req.post("http://api.cloudinary.com/v1_1/dhan3kbrs/auto/upload", data=things)
        response = uplode.json()
        photo_name = response["public_id"]
        url = response["secure_url"]
        return "<h1>PHOTO ID: %s</h1><img src='%s'></img><h5>%s</h5>" % (photo_name, url, url)

if __name__ == "__main__":
    app.run()

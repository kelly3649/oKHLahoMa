from flask import Flask, render_template, request
import requests as req

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("nootnoot.html")
    else:
        things = { "file" : request.form["sneaky"], "upload_preset" : "bf17cjwp" }
        uplode = req.post("https://api.cloudinary.com/v1_1/dhan3kbrs/auto/upload", params=things)
        return uplode.text

if __name__ == "__main__":
    app.run()

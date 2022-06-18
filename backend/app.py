from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
from backend import liked, subscriptions, authentication
import pickle



app = Flask(__name__, template_folder='../templates', static_folder='../static')
token_file = "../token.pickle"


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('log') == "login":
            authentication.oauth()
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        with open(token_file, "rb") as token:
            cred = pickle.load(token)
        youtube = build("youtube", 'v3', credentials=cred)
        if request.form.get('sub') == 'subscriptions':
            sub = subscriptions.subscribed_channels(youtube)
            return render_template("index.html", pref=str(sub))
        if request.form.get('liked') == 'liked_pl':
            liked_pl = liked.liked_playlist(youtube)
            return render_template("index.html", pref=str(liked_pl))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

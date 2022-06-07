from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
import liked
import subscriptions
import authentication

app = Flask(__name__)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('log') == "Login using Google account":
            return redirect(url_for('index'))
    else:
        return render_template("login.html")


@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        cred = authentication.oauth()
        youtube = build("youtube", 'v3', credentials=cred)
        if request.form.get('sub') == 'Subscriptions':
            sub = subscriptions.subscribed_channels(youtube)
            return render_template("index.html", pref=str(sub))
        if request.form.get('liked') == 'Liked Playlists':
            liked_pl = liked.liked_playlist(youtube)
            return render_template("index.html", pref=str(liked_pl))
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

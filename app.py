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
            cred = authentication.oauth()
            yt = build("youtube", 'v3', credentials=cred)
            return redirect(url_for('index', youtube=yt))
    return render_template("login.html")


@app.route('/index/<youtube>', methods=['POST', 'GET'])
def index(youtube):
    print(request.method)
    if request.method == 'POST':
        print("wow")
        if request.form.get('sub') == 'Subscriptions':
            print(youtube)
            sub = subscriptions.subscribed_channels(youtube)

            return str(sub)  # do something
        elif request.form.get('liked') == 'Liked Playlists':
            liked_pl = liked.liked_playlist(youtube)
            return str(liked_pl)  # do something else
    elif request.method == 'GET':
        print("a")
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

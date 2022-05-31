from flask import Flask, render_template
from googleapiclient.discovery import build
import liked
import subscriptions
import authentication


liked_playlist = True
subscribed = False
cred = authentication.oauth()
youtube = build("youtube", 'v3', credentials=cred)
if liked_playlist:
    liked_pl = liked.liked_playlist(youtube)
if subscribed:
    sub = subscriptions.subscribed_channels(youtube)

app = Flask(__name__)

@app.route('/')
def index():
    return str(liked_pl)

if __name__ == "__main__":
    app.run(debug=True)

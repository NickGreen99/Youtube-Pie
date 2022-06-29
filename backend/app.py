from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
import liked, subscriptions, authentication
import pickle
import random
import json
import os
from pathlib import Path


app = Flask(__name__, template_folder='../templates', static_folder='../static')
token_folder = Path(__file__).parent.parent
token_file = token_folder / "token.pickle"


def percentages(categories):  # Sort labels and sizes to create better pie chart
    labels = []
    sizes = []
    num = len(categories)
    for i in categories:
        if i not in labels:
            labels.append(i)
            count = 0
            for j in categories:
                if j == i:
                    count += 1
            sizes.append(count / num)
    n = len(labels)
    color = ["#" + ''.join([random.choice('0123456789ABCDEF')
                            for j in range(6)]) for i in range(n)]
    for i in range(0, len(sizes) - 1):
        sizes[i] = sizes[i] * 100
    return labels, sizes, color


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get('log') == "login":
            authentication.oauth()
            return redirect(url_for("callback"))
    return render_template("login.html", logged_in=False)


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'POST':
        with open(token_file, "rb") as token:
            cred = pickle.load(token)
        youtube = build("youtube", 'v3', credentials=cred)
        if request.form.get('sub') == 'subscriptions':
            sub = subscriptions.subscribed_channels(youtube)
            labels, sizes, colors = percentages(sub)
            return render_template("index.html", pref='sub', labels=json.dumps(labels), sizes=json.dumps(sizes),
                                   colors=json.dumps(colors))
        if request.form.get('liked') == 'liked_pl':
            liked_pl = liked.liked_playlist(youtube)
            labels, sizes, colors = percentages(liked_pl)
            return render_template("index.html", pref='liked', labels=json.dumps(labels), sizes=json.dumps(sizes),
                                   colors=json.dumps(colors))
    return render_template("login.html", logged_in=True)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

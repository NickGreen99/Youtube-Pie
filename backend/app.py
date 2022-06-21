from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
import liked, subscriptions, authentication
import pickle
import random

app = Flask(__name__, template_folder='../templates', static_folder='../static')
token_file = "../token.pickle"


def percentages(categories):
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
    labels = [f'{l}, {s:0.2f}%' for l, s in zip(labels, sizes)]
    return labels,sizes,color

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
            return render_template("index.html", pref='sub', chart_data = sub)
        if request.form.get('liked') == 'liked_pl':
            liked_pl = liked.liked_playlist(youtube)
            return render_template("index.html", pref='liked', chart_data = liked_pl)
    return render_template("login.html", logged_in=True)


if __name__ == "__main__":
    app.run(debug=True)

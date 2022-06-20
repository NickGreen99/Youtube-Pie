from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build
import liked, subscriptions, authentication
import pickle
import matplotlib.pyplot as plt
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
    plt_1 = plt.figure(figsize=(7, 4))
    plt.pie(sizes, shadow=True, startangle=90, colors=color)
    for i in range(0, len(sizes) - 1):
        sizes[i] = sizes[i] * 100
    labels = [f'{l}, {s:0.2f}%' for l, s in zip(labels, sizes)]
    plt.legend(bbox_to_anchor=(0.1, 0.5), loc='center right', labels=labels)
    plt.tight_layout()
    plt.savefig('../static/images/demo.png', transparent=True)
    plt.show()


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
            sub, total_sub = subscriptions.subscribed_channels(youtube)
            percentages(total_sub)
            return render_template("index.html", pref=str(sub))
        if request.form.get('liked') == 'liked_pl':
            liked_pl, total_liked = liked.liked_playlist(youtube)
            percentages(total_liked)
            return render_template("index.html", pref=str(liked_pl))
    return render_template("login.html", logged_in=True)


if __name__ == "__main__":
    app.run(debug=True)

import flask
import liked, subscriptions
import random
import json
import os
from pathlib import Path

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# App
app = flask.Flask(__name__, template_folder='../templates', static_folder='../static')

client_secrets_folder = Path(__file__).parent.parent
CLIENT_SECRETS_FILE = client_secrets_folder / "client_secrets/client_secrets.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

app.secret_key = 'REPLACE ME - this value is here as a placeholder.'


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


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
    for i in range(0, len(sizes)):
        sizes[i] = sizes[i] * 100
        sizes[i] = round(sizes[i], 1)
    sizes, labels = zip(*sorted(zip(sizes, labels)))
    sizes = list(sizes)
    labels = list(labels)
    sizes.reverse()
    labels.reverse()
    return labels, sizes, color


@app.route('/', methods=['POST', 'GET'])
def login():
    if flask.request.method == 'POST':
        if 'credentials' not in flask.session:
            return flask.redirect('authorize')
        return flask.redirect('stats')

    return flask.render_template("login.html", logged_in=False)


@app.route('/stats', methods=['POST', 'GET'])
def user_profile():
    try:
        # Load credentials from the session.
        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])
        youtube = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials)
        if flask.request.method == 'POST':
            if flask.request.form.get('sub') == 'subscriptions':
                sub = subscriptions.subscribed_channels(youtube)
                labels, sizes, colors = percentages(sub)
                return flask.render_template("index.html", pref='sub', labels=json.dumps(labels),
                                             sizes=json.dumps(sizes),
                                             colors=json.dumps(colors))
            if flask.request.form.get('liked') == 'liked_pl':
                liked_pl = liked.liked_playlist(youtube)
                labels, sizes, colors = percentages(liked_pl)
                return flask.render_template("index.html", pref='liked', labels=json.dumps(labels),
                                             sizes=json.dumps(sizes),
                                             colors=json.dumps(colors))
            if flask.request.form.get('logout') == 'logout':
                return flask.redirect('clear')
            # Save credentials back to session in case access token was refreshed.
            # ACTION ITEM: In a production app, you likely want to save these
            #              credentials in a persistent database instead.

        flask.session['credentials'] = credentials_to_dict(credentials)
        return flask.render_template("login.html", logged_in=True)
    except KeyError as e:
        return flask.redirect('/')


@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('user_profile'))


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return flask.redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run(host='0.0.0.0', port=port)
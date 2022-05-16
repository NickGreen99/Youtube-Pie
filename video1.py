from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import json

API_KEY = 'AIzaSyD6NtHkQbmFYG13fvkQxH4EiWld7AKKYlI'

# Oauth 2.0 authentication

credentials = None

# token.pickle stores the user's credentials from previously successful login
if os.path.exists("token.pickle"):
    print("Loading Credentials from File...")
    with open("token.pickle", "rb") as token:
        credentials = pickle.load(token)

# if there are no valid credentials available, then either refresh the token or create new one
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing Access Token...")
        credentials.refresh(Request())
    else:
        print("Fetching new Tokens...")
    # Select the scopes of our app
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube.readonly"])

    # Create server (localhost this time) to prompt users to allow us to view their YoutTube data
    flow.run_local_server(port=8080, prompt="consent")

    # Acquire credentials
    credentials = flow.credentials

    # Save the credentiasls for the next run
    with open("token.pickle", "wb") as f:
        print("Saving Credentials for future Use...")
        pickle.dump(credentials, f)

    print(credentials.to_json())

youtube = build("youtube", 'v3', credentials=credentials)

# Get all account subscriptions (use paging)
nextPageToken = None
channels = []
while True:
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        channelId="UCn3kl6oCqZIaloJsVBgQLpw",
        prettyPrint=True,
        alt="json",
        maxResults=50,
        pageToken=nextPageToken
    )
    response_subscriptions = request.execute()
    for item in response_subscriptions['items']:
        channels.append(item['snippet'])
    nextPageToken = response_subscriptions.get('nextPageToken')
    if not nextPageToken:
        break

categories = {}
categoryname=[]
for channel in channels:
    channel_id = channel['resourceId']['channelId']
    # get channel uploads
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response_uploads = request.execute()

    try:
        # get video ids
        uploads_id = response_uploads['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_id,
            maxResults=1
        )
        response_videoid = request.execute()
        videoid = response_videoid['items'][0]['snippet']['resourceId']['videoId']

        # get video category id
        request = youtube.videos().list(
            part='snippet',
            id=videoid
        )
        response_categoryid = request.execute()
        categoryid = response_categoryid['items'][0]['snippet']['categoryId']

        # get video category name
        request = youtube.videoCategories().list(
            part='snippet',
            id=categoryid
        )
        response_categoryname = request.execute()
        categoryname.append(response_categoryname['items'][0]['snippet']['title'])

    except:
        continue

# create dictionary to keep track of category instances
for key in categoryname:
    if key in categories.keys():
        categories[key] = categories[key] + 1
    else:
        categories.update(({key:1}))

# sort dictionary and create list of your preferred categories
ordered_cat = dict(sorted(categories.items(),key=lambda item: item[1]))
category_list = list(ordered_cat.keys())
category_list.reverse()
print(category_list)


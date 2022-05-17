from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os


#API_KEY = 'AIzaSyD6NtHkQbmFYG13fvkQxH4EiWld7AKKYlI'


def create_category_dict(category_list):
    categories_dict = {}
    for key in category_list:
        if key in categories_dict.keys():
            categories_dict[key] = categories_dict[key] + 1
        else:
            categories_dict.update(({key: 1}))
    return categories_dict


def create_preferred_list(categories_dict):
    ordered_cat = dict(sorted(categories_dict.items(), key=lambda item: item[1]))
    category_list = list(ordered_cat.keys())
    category_list.reverse()
    return category_list

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

# Get 'liked videos' playlist from account
request = youtube.channels().list(
    part="contentDetails",
    mine="True",
)
response_liked = request.execute()

liked_videos = []
nextPageToken = None
i = 1
while True:
    try:
        # get video ids
        liked_id = response_liked['items'][0]['contentDetails']['relatedPlaylists']['likes']
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=liked_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        response_videoid = request.execute()
        for i in range(0, len(response_videoid['items'])):
            videoid = response_videoid['items'][i]['snippet']['resourceId']['videoId']
            liked_videos.append(videoid)
        nextPageToken = response_videoid.get('nextPageToken')
        if not nextPageToken:
            break
    except:
        continue
liked_categoryname = []
for video in liked_videos:
    try:
        # get video category id
        request = youtube.videos().list(
            part='snippet',
            id=video
        )
        response_categoryid = request.execute()
        categoryid = response_categoryid['items'][0]['snippet']['categoryId']

        # get video category name
        request = youtube.videoCategories().list(
            part='snippet',
            id=categoryid
        )
        response_categoryname = request.execute()
        liked_categoryname.append(response_categoryname['items'][0]['snippet']['title'])
    except:
        continue
categories = create_category_dict(liked_categoryname)
preferences = create_preferred_list(categories)


# Get all account subscriptions (use paging)
nextPageToken = None
channels = []
while True:
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        mine="True",
        maxResults=50,
        pageToken=nextPageToken
    )
    response_subscriptions = request.execute()
    for item in response_subscriptions['items']:
        channels.append(item['snippet'])
    nextPageToken = response_subscriptions.get('nextPageToken')
    if not nextPageToken:
        break

categoryname = []
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
categories = create_category_dict(categoryname)

# sort dictionary and create list of your preferred categories
preferences = create_preferred_list(categories)
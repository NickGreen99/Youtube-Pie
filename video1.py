from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import json

API_KEY = 'AIzaSyD6NtHkQbmFYG13fvkQxH4EiWld7AKKYlI'

##  Oauth 2.0 authentication

credentials = None

# token.pickle stores the user's credentials from previously succesful login
if os.path.exists("token.pickle"):
    print("Loading Credentials from File...")
    with open("token.pickle","rb") as token:
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
    with open("token.pickle","wb") as f:
        print("Saving Credentials for future Use...")
        pickle.dump(credentials,f)

    print(credentials.to_json())

youtube = build("youtube", 'v3', credentials=credentials)

nextPageToken=None
# x=[]
# while True:
#     request = youtube.subscriptions().list(
#         part="snippet,contentDetails",
#         channelId="UCn3kl6oCqZIaloJsVBgQLpw",
#         prettyPrint=True,
#         alt="json",
#         maxResults=50,
#         pageToken=nextPageToken
#     )
#     response=request.execute()
#     for item in response['items']:
#         x.append(item['snippet'])
#     nextPageToken = response.get('nextPageToken')
#     if not nextPageToken:
#         break
# print(x)
request = youtube.subscriptions().list(
    part="snippet,contentDetails",
    channelId="UCn3kl6oCqZIaloJsVBgQLpw",
    prettyPrint=True,
    alt="json",
    maxResults=50,
    pageToken=nextPageToken
)
response = request.execute()
print(response['items'][0]['snippet'])
y_id=response['items'][0]['snippet']['resourceId']['channelId']
print('\n')
request = youtube.channels().list(
    part="snippet,topicDetails",
    id=y_id,
    prettyPrint=True,
)
response = request.execute()
print(response)
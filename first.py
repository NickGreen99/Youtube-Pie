from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# API_KEY = 'AIzaSyD6NtHkQbmFYG13fvkQxH4EiWld7AKKYlI'

##  Oauth 2.0 authentication

# Select the scopes of our app
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube.readonly"])

# Create server (localhost this time) to prompt users to allow us to view their YoutTube data
flow.run_local_server(port=8080, prompt="consent")

# Acquire credentials
credentials = flow.credentials

print(credentials.to_json())

# youtube = build("youtube", 'v3', developerKey=API_KEY)
#
# request = youtube.channels().list(
#     part='statistics',
#     forUsername='schafer5'
# )
#
#
# response=request.execute()
# print(response)

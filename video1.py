from urllib import response
from googleapiclient.discovery import build

import os

api_key = os.environ.get("GoogleAPIKey")

youtube = build("youtube","v3", developerKey= api_key)

request = youtube.channels().list(
        part = "statistics",
        id = 'UC5ZZcLjzSCPga1LRYXylBhA' #different from username that used in tutorial its mine

    )

response = request.execute()

print(response)
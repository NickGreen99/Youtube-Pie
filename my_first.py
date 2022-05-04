from urllib import response
from googleapiclient.discovery import build



api_key = "AIzaSyCN4ZO-zHb71wGlkJE8ZhSbIzs9GVyxrU0"

youtube = build("youtube","v3", developerKey= api_key)

request = youtube.channels().list(
        part = "statistics",
        id = 'UC5ZZcLjzSCPga1LRYXylBhA' #different from username that used in tutorial

    )

response = request.execute()

print(response)
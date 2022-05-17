from googleapiclient.discovery import build
import liked
import subscriptions
import authentication

if __name__== "__main__":
    liked_playlist = False
    subscribed = True
    cred = authentication.oauth()
    youtube = build("youtube", 'v3', credentials=cred)
    if liked_playlist:
        liked_pl = liked.liked_playlist(youtube)
    if subscribed:
        sub = subscriptions.subscribed_channels(youtube)
from googleapiclient.discovery import build
import liked
import subscriptions
import authentication

if __name__== "__main__":
    liked_playlist = True
    subscribed = False
    cred = authentication.oauth()
    youtube = build("youtube", 'v3', credentials=cred)
    if liked_playlist:
        liked_pl = liked.liked_playlist(youtube)
        print(liked_pl)
    if subscribed:
        sub = subscriptions.subscribed_channels(youtube)
        print(sub)
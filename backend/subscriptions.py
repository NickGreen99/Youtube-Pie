from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

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
def subscribed_channels(youtube):
    # Get all account subscriptions (use paging)
    next_page_token = None
    channels = []
    while True:
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine="True",
            maxResults=50,
            pageToken=next_page_token
        )
        response_subscriptions = request.execute()
        for item in response_subscriptions['items']:
            channels.append(item['snippet'])
        if len(channels) >= 50:
            break
        next_page_token = response_subscriptions.get('nextPageToken')
        if not next_page_token:
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

        except Exception as e:
            continue

    # create dictionary to keep track of category instances
    categories = create_category_dict(categoryname)

    # sort dictionary and create list of your preferred categories
    return create_preferred_list(categories)

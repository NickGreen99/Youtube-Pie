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
        # limit channels to 50
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

    return categoryname

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


def liked_playlist(youtube):
    # Get 'liked videos' playlist from account
    request = youtube.channels().list(
        part="contentDetails",
        mine="True",
    )
    response_liked = request.execute()

    liked_videos = []
    next_page_token = None
    while True:
        try:
            # get video ids
            liked_id = response_liked['items'][0]['contentDetails']['relatedPlaylists']['likes']
            request = youtube.playlistItems().list(
                part='snippet',
                playlistId=liked_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response_videoid = request.execute()
            for i in range(0, len(response_videoid['items'])):
                videoid = response_videoid['items'][i]['snippet']['resourceId']['videoId']
                liked_videos.append(videoid)
            if len(liked_videos) >= 200:
                break
            next_page_token = response_videoid.get('nextPageToken')
            if not next_page_token:
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
        except Exception as e:
            continue
    categories = create_category_dict(liked_categoryname)
    return create_preferred_list(categories)

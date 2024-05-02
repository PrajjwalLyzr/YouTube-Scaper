from datetime import datetime
from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv; load_dotenv()

if not os.path.exists('data'):
    os.makedirs('data')

def get_channel_id(youtube, channel_id):

    request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        id=channel_id)
    
    response = request.execute()    
    playlist_id =  response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return playlist_id



def get_videos_ids(youtube, playlist_id):

    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId = playlist_id,
        maxResults = 50)
    
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    return video_ids


def get_video_details(youtube, video_ids):

    video_urls = []
    titles = []
    dates = []
    views = []
    likes = []


    request = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids))

    response = request.execute()

    for video in response['items']:
        video_urls.append(f"https://www.youtube.com/watch?v={video['id']}"),
        titles.append(video['snippet']['title']),
        date = datetime.strptime(str(video['snippet']['publishedAt']), '%Y-%m-%dT%H:%M:%SZ')
        dates.append(date.date()),
        views.append(video['statistics']['viewCount']),
        likes.append(video['statistics']['likeCount'])
        

    return video_urls, titles, dates, views, likes


def csv_maker(dates, titles, likes, views, video_urls, filename):
    data_items = {
        'Published Date':dates,
        'Titles': titles,
        'Likes':likes,
        'Views':views,
        'Urls':video_urls,
    }

    df = pd.DataFrame(data_items)
    df.to_csv(f"data/{filename}.csv", index=False)



if __name__ == "__main__":
    api_key = os.getenv('YT_API_KEY')

    # change this id according to the channel you want to scrape on every run.
    channel_id = "UCNU_lfiiWBdtULKOw6X0Dig" #krish naik channel id

    # modify the channel_name as per your choice
    channel_name = 'KrishNaik'

    youtube = build(serviceName='youtube', version='v3', developerKey=api_key)
    id = get_channel_id(youtube=youtube, channel_id=channel_id)
    vdo_ids = get_videos_ids(youtube=youtube, playlist_id=id)
    video_urls, titles, dates, views, likes = get_video_details(youtube=youtube, video_ids= vdo_ids)
    csv_maker(dates, titles, likes, views, video_urls, filename=channel_name)

    
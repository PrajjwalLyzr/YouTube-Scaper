from datetime import datetime
from googleapiclient.discovery import build
import isodate
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
        playlistId=playlist_id,
        maxResults=50)

    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_id = response['items'][i]['contentDetails']['videoId']
        

        video_request = youtube.videos().list(
            part='contentDetails',
            id=video_id
        )
        video_response = video_request.execute()
        duration = video_response['items'][0]['contentDetails']['duration']
        

        # Convert ISO 8601 duration to seconds
        duration_seconds = isodate.parse_duration(duration).total_seconds()
        
        # Exclude videos with duration less than 4 minutes (240 seconds)
        if duration_seconds >= 240:
            video_ids.append(video_id)
    
    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request  =  youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken = next_page_token)
            
            response = request.execute()

            for i in range(len(response['items'])):
                video_id = response['items'][i]['contentDetails']['videoId']
                

                video_request = youtube.videos().list(
                    part='contentDetails',
                    id=video_id
                )
                video_response = video_request.execute()
                duration = video_response['items'][0]['contentDetails']['duration']
               
                # Convert ISO 8601 duration to seconds
                duration_seconds = isodate.parse_duration(duration).total_seconds()
               
                # Exclude videos with duration less than 4 minutes (240 seconds)
               
                if duration_seconds >= 240:
                    video_ids.append(video_id)

            next_page_token = response.get('nextPageToken')

    return video_ids


def get_video_details(youtube, video_ids):

    video_urls = []
    titles = []
    dates = []
    views = []
    likes = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50]))

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
    channel_id = "UCYSbIYzulx3HT5_OQLUH38A" #Jason M. Lemkin channel id

    # channel_id = "UCNU_lfiiWBdtULKOw6X0Dig" #krish naik id


    # modify the channel_name as per your choice
    channel_name = 'JasonLemkin4MIN'

    youtube = build(serviceName='youtube', version='v3', developerKey=api_key)
    id = get_channel_id(youtube=youtube, channel_id=channel_id)
    vdo_ids = get_videos_ids(youtube=youtube, playlist_id=id)
    video_urls, titles, dates, views, likes = get_video_details(youtube=youtube, video_ids= vdo_ids)
    csv_maker(dates, titles, likes, views, video_urls, filename=channel_name)

    
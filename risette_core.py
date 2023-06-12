#===================================================================#
#                                                                   #
#    Risette.py's core -- What makes the web app work, the engine   #
#    risette_core.py Pre-alpha version                              #
#                                                                   #
#-------------------------------------------------------------------#
#                                                                   #
#    Arturo Olivares                                                #
#                                                                   #
#   Copyright (C) 2023 Arturo Olivares                              #
#   GNU GPLv3                                                       #
#                                                                   #
#===================================================================#

import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from datetime import datetime, timedelta
from isodate import parse_duration
import pandas as pd

class Service:
    def __init__(self, serviceName: str, version: str, developerKey=None):
        self.serviceName = serviceName
        self.version = version
        self.developerKey = developerKey

    def build_service(self):
        if self.developerKey == None:
            return None

        service = build(self.serviceName, self.version, developerKey=self.developerKey)
        return service

# get_channel_id v.2.1 (Safe version)
def get_channel_id(url: str = None) -> str:
    """
    Gets the ID of a YouTube channel from its URL.

    Args:
        URL (str): YouTube's channel URL
        
        The URL can be of the following types:

        From https://support.google.com/youtube/answer/6180214?hl=en-GB

        - Handle URL
            
            Example: youtube.com/@youtubecreators

            A handle URL is created automatically whenever you choose or change your handle as a channel owner. 
            The end of the URL starts with an '@' symbol and includes your chosen handle. Any custom URLs that you 
            may already have will continue to work.

        - Customised URL

            Example: youtube.com/c/YouTubeCreators

            New custom URLs can no longer be set up or changed. Any custom URLs that you may already have will continue to work. 
            All legacy URLs now redirect users to your new channel URL that is based on your handle. 

        - Legacy username URL

            Example: youtube.com/user/YouTube

            Depending on when your channel was created, it may have a username. Usernames are no longer required for channels 
            today, but you can still use this URL to direct viewers to your channel. This also includes if your channel 
            name has changed since you chose your username. Existing usernames can't be changed.

    Returns:
        str: YouTube's channel ID or an error message if the ID could not be retrieved
    """

    if url is None:
        return "[Error]. You must provide a YouTube channel's URL."
    
    # v.2.1
    response = requests.get(url)

    if response == "<Response [404]>":
        return "Error 404"
    
    html = response.text
    
    for i in range(7):

        # v.2 -- Deactivated
        # response = requests.get(URL)
        # html = response.text

        parser = BeautifulSoup(html, "html.parser")
        meta_tag = parser.find("meta", attrs={"name": "twitter:url"})

        try:
            content_value = meta_tag.get("content")
            channel_id = content_value.split("/")[-1]
            return channel_id
        except (AttributeError, IndexError):
            continue
        
    return "Error 404"

def get_channel_details(service: Resource, channelID: str = None) -> (tuple | str):
    """
    Retrieves details of a YouTube channel.

    Args:
        service (Resource): The YouTube service Resource obtained from 'googleapiclient.discovery'
        channelID (str, optional): The ID of the YouTube channel. Defaults to None.
    
    Returns:
        tuple or str: A tuple containing the following channel details:
            - YouTube channel's name
            - YouTube channel's profile pic URL
            - YouTube channel's banner URL
            - YouTube channel's description
            - YouTube channel's country of origin
            - YouTube channel's creation date
            - YouTube channel's total views
            - YouTube channel's total amount of videos
            - YouTube channel's approximate amount of subscribers
        If an error occurs, it returns an error string.

    Raises:
        None
    """

    if channelID is None:
        return "[Error]. You must provide a YouTube channel's ID."
    
    try:
        response = service.channels().list(
            part='snippet, brandingSettings, statistics, contentDetails',
            id=channelID
        ).execute()

        return (
                response['items'][0]['snippet']['title'], # YouTube channel's name
                response['items'][0]['snippet']['thumbnails']['default']['url'], # YouTube channel's profile pic URL 
                response['items'][0]['brandingSettings']['image']['bannerExternalUrl'], # YouTube channel's banner URL
                response['items'][0]['snippet']['description'], # YouTube channel's description
                response['items'][0]['snippet']['country'], # YouTube channel's country of origin 
                response['items'][0]['snippet']['publishedAt'], # YouTube channel's creation date 
                int(response['items'][0]['statistics']['viewCount']), # YouTube channel's total views
                int(response['items'][0]['statistics']['videoCount']), #YouTube channel's total amount of videos
                int(response['items'][0]['statistics']['subscriberCount']) # YouTube channel's aprox. amount of subs.
            )

    except Exception as error:
        return f"[Error]. {error}"

def iso8601_to_prettydate(date: str) -> str:
    """
    Converts a string date in ISO 8601 format into a more readable format.

    Args:
        date (str): ISO 8601-date string ('YYYY-MM-DDTHH:MM:SSZ').
    
    Returns:
        str: Date string in the following format ('Month DD, YYYY')

    Example:
    >>> iso8601_to_prettydate('2009-04-30T19:37:51Z')
    'April 30, 2009'
    """

    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d, %Y')


def get_relevant_vids(service: Resource, channelID: str = None) -> (tuple | str):
    """
    Retrieves relevant video IDs from a YouTube channel.

    Args:
        service (Resource): The YouTube service resource obtained from 'googleapiclient.discovery.build'.
        channelID (str, optional): The ID of the YouTube channel. Defaults to None.

    Returns:
        tuple[str]: A tuple containing the following relevant video IDs:
            - Latest video ID (based on upload date)
            - Most viewed video ID
            - Oldest video ID (posted after channel creation)
        The function fetches the latest video ID, most viewed video ID, and the oldest video ID (posted after the channel's creation date).
        If an error occurs, it returns an error string.

    Raises:
        None
    """

    if channelID is None:
        return "[Error]. You must provide a YouTube channel's ID."

    try:
        # Fetch the latest YT channel's video ID
        response = service.search().list(
            part='id',
            channelId=channelID,
            order='date',
            type='video'
        ).execute()
        latest_video_id = response['items'][0]['id']['videoId']

        # Fetch the most popular YT channel's video ID
        response = service.search().list(
            part='id',
            channelId=channelID,
            order='viewCount',
            type='video'
        ).execute()
        most_viewed_video_id = response['items'][0]['id']['videoId']

        # Fetch the oldest YT channel's video ID
        response = service.channels().list(
            part='snippet',
            id=channelID
        ).execute()
        channel_created_at = datetime.fromisoformat(response['items'][0]['snippet']['publishedAt'])

        # Find channel videos posted after the creation date
        published_before = channel_created_at + timedelta(days=365)  # Add a year
        search_response = service.search().list(
            part='id',
            channelId=channelID,
            publishedAfter=channel_created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
            publishedBefore=published_before.strftime('%Y-%m-%dT%H:%M:%SZ'),
            type='video'
        ).execute()

        while len(search_response['items']) == 0:
            channel_created_at = published_before
            published_before = channel_created_at + timedelta(days=365)  # Add a year
            search_response = service.search().list(
                part='id',
                channelId=channelID,
                publishedAfter=channel_created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                publishedBefore=published_before.strftime('%Y-%m-%dT%H:%M:%SZ'),
                type='video'
            ).execute()

        oldest_video_id = search_response['items'][0]['id']['videoId']

        return (latest_video_id, most_viewed_video_id, oldest_video_id)

    except Exception as error:
        return f"[Error]. {error}"


def get_video_details(service: Resource, videoID: str, lightMode: bool = False) -> tuple:
    """
    Retrieves details of a video using its ID.

    Args:
        service (Resource): The service resource used for making API requests.
        videoID (str): The ID of the video for which details are to be retrieved.
        lightMode (bool, optional): Indicates whether to retrieve limited details (default: False).

    Returns:
        tuple: A tuple containing the video details based on the provided parameters.
               If lightMode is False, the tuple will contain (title, description, views, likes).
               If lightMode is True, the tuple will contain (title, duration, likes).
    """

    request = service.videos().list(
        part = 'snippet,statistics,contentDetails',
        id = videoID
    )

    response = request.execute()

    video_details = response['items'][0]

    if lightMode is False:
        title = video_details['snippet']['title']
        description = video_details['snippet']['description']
        views = int(video_details['statistics']['viewCount'])
        likes = int(video_details['statistics']['likeCount'])
        
        """
        Note: The statistics.dislikeCount property was made private as of December 13, 2021. 
        This means that the property is included in an API response only if the API request was 
        authenticated by the video owner. See the revision history for more information.
        """

        #dislikes = int(video_details['statistics']['dislikeCount'])

        return (title, description, views, likes)
    
    video_details = response['items'][0]
    title = video_details['snippet']['title']
    duration = video_details['contentDetails']['duration']
    likes = int(video_details['statistics']['likeCount'])

    return (title, duration, likes)
    
def get_uploads_id(service: Resource, channelID: str = None) -> str:
    """
    Retrieves the uploads playlist ID for a YouTube channel using the channel ID.

    Args:
        service (Resource): The service resource used for making API requests.
        channelID (str, optional): The ID of the YouTube channel (default: None).

    Returns:
        str: The uploads playlist ID of the specified YouTube channel.
             Returns an error message if the channel ID is not provided or an exception occurs.
    """
        
    if channelID is None:
        return "[Error]. You must provide a YouTube channel's ID."
    
    try:
        request = service.channels().list(
                part='snippet, contentDetails, statistics',
                id=channelID)
        response = request.execute()
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    except Exception as error:
        return f"[Error]. {error}"
 

def get_latest_vids_ids(service: Resource, playlistID: str) -> list:
    """
    Retrieves the video IDs of the latest videos in a playlist using its ID.

    Args:
        service (Resource): The service resource used for making API requests.
        playlistID (str): The ID of the playlist.

    Returns:
        list: A list of video IDs of the latest videos in the specified playlist.
    """

    videoIDs = []

    request = service.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlistID,
        maxResults = 50
    )
    response = request.execute()

    for item in response['items']:
        videoIDs.append(item['contentDetails']['videoId'])

    """
    Limit to 50 videos only to reduce API request costs
    
    next_page_token = response.get('nextPageToken')
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId = playlist_id,
        maxResults = 50,
        pageToken = next_page_token
    )
    response = request.execute()

    for item in response['items']:
        videoIDs.append(item['contentDetails']['videoId'])

    """
    return videoIDs


def get_latestvids_dataframe(service: Resource, playlistID: str) -> pd.DataFrame:
    """
    Retrieves the details of the latest videos in a playlist and returns them as a pandas DataFrame.

    Args:
        service (Resource): The service resource used for making API requests.
        playlistID (str): The ID of the playlist.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the details of the latest videos.
                      The DataFrame has columns for 'Title', 'Duration', and 'Likes'.
    """

    videoIDs = get_latest_vids_ids(service, playlistID)
    videosData = []

    for videoID in videoIDs:
        videoDetails = get_video_details(service, videoID, lightMode=True)
        videosData.append(videoDetails)

    dataFrame = pd.DataFrame(videosData, columns=['Title', 'Duration', 'Likes'])

    return dataFrame


def iso8601_to_min(durationStr: str) -> float:
    """
    Converts an ISO 8601 duration string to minutes.

    Args:
        durationStr (str): The duration string in ISO 8601 format.

    Returns:
        float: The duration in minutes.

    Example:
        >>> iso8601_to_min('PT1H30M')
        90.0
        >>> iso8601_to_min('P3DT2H30M')
        4380.0
    """

    return parse_duration(durationStr).total_seconds() / 60

def sort_df_by_duration(dataFrame: pd.DataFrame, descending: bool=True, sample: int = 20) -> pd.DataFrame:
    """
    Sorts a Pandas DataFrame by the 'Duration' column in either ascending or descending order 
    and returns a sample of the sorted DataFrame.

    Args:
        dataFrame (pd.DataFrame): The input DataFrame to be sorted.
        descending (bool, optional): Determines the sorting order. 
                                     If True (default), sorts the DataFrame in descending order. 
                                     If False, sorts in ascending order.
        sample (int, optional): The number of rows to return as a sample of the sorted DataFrame. Defaults to 20.

    Returns:
        pd.DataFrame: The sorted DataFrame with a specified sample size.
    """
    dataFrame['Duration (min)'] = dataFrame['Duration'].apply(iso8601_to_min)
    
    if descending:
        return dataFrame.sort_values(by='Duration (min)', ascending=False).head(sample) # Sorted data frame (descending)

    return dataFrame.sort_values(by='Duration (min)', ascending=True).head(sample) # Sorted data frame (ascending)


def sort_df_by_likes(dataFrame: pd.DataFrame, descending: bool=True, sample: int = 20) -> pd.DataFrame:
    """
    Sorts a Pandas DataFrame by the 'Likes' column in either ascending or descending order 
    and returns a sample of the sorted DataFrame.

    Args:
        dataFrame (pd.DataFrame): The input DataFrame to be sorted.
        descending (bool, optional): Determines the sorting order. 
                                     If True (default), sorts the DataFrame in descending order. 
                                     If False, sorts in ascending order.
        sample (int, optional): The number of rows to return as a sample of the sorted DataFrame. Defaults to 20.

    Returns:
        pd.DataFrame: The sorted DataFrame with a specified sample size.
    """

    if descending:
        return dataFrame.sort_values(by='Likes', ascending=False).head(sample) # Sorted data frame (descending)

    return dataFrame.sort_values(by='Likes', ascending=True).head(sample) # Sorted data frame (ascending)

# ARCHIVE

"""
    get_channel_id v.1 (Safe version) [Depracated - OBSOLETE]

    def get_channel_id(URL=None):
        if URL is None:
            return "[Error]. You must provide a YouTube channel's URL."
        

        for i in range(7):
            response = requests.get(URL)
            html = response.text

            parser = BeautifulSoup(html, "html.parser")
            meta_tag = parser.find("meta", itemprop="channelId")

            try:
                content_value = meta_tag.get("content")
                return content_value
            except AttributeError:
                continue

        return "[Error]. Could not retrieve channel ID"
"""
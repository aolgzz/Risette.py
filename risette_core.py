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
from hades import cerberus
from datetime import datetime

# get_channel_id v.2.1 (Safe version)
def get_channel_id(URL=None) -> str:
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

    if URL is None:
        return "[Error]. You must provide a YouTube channel's URL."
    
    # v.2.1
    response = requests.get(URL)

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


class Service:
    def __init__(self, serviceName, version, developerKey=None):
        self.serviceName = serviceName
        self.version = version
        self.developerKey = developerKey

    def build_service(self):
        if self.developerKey == None:
            return None

        service = build(self.serviceName, self.version, developerKey=self.developerKey)
        return service

def get_channel_details(service, channel_id=None):
    if channel_id is None:
        return "[Error]. You must provide a YouTube channel's ID."
    
    try:
        response = service.channels().list(
            part='snippet, brandingSettings, statistics, contentDetails',
            id=channel_id
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
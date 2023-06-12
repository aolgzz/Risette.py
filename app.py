#===================================================================#
#                                                                   #
#    Risette.py's -- A lightweight Flask app                        #
#    app.py Pre-alpha version                                       #
#                                                                   #
#-------------------------------------------------------------------#
#                                                                   #
#    Arturo Olivares                                                #
#                                                                   #
#   Copyright (C) 2023 Arturo Olivares                              #
#   GNU GPLv3                                                       #
#                                                                   #
#===================================================================#

from flask import Flask, render_template, request
from risette_core import get_channel_id, Service, get_channel_details, iso8601_to_prettydate
from risette_core import get_relevant_vids, getVideoDetails
from hades import cerberus

#Replace cerberus with your API key
youtube = Service('youtube', 'v3', cerberus).build_service()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/analysisResult", methods=["POST"])
def result():
    URL = request.form["channel_url"]
    
    channel_id = get_channel_id(URL)

    if channel_id == "Error 404":
        error_message = "Error 404. YouTube channel not found"
        return render_template('index.html', error_message=error_message)
    
    #API disconnected mode: OFF
    #"""
    
    channelAbout = get_channel_details(youtube, get_channel_id(URL))
    creationDate = iso8601_to_prettydate(channelAbout[5])

    relVidsIDs = get_relevant_vids(youtube, channel_id)
    relVidsInfo = {}

    for i, videoID in enumerate(relVidsIDs, start=1):
        videoData = getVideoDetails(youtube, videoID)
        relVidsInfo[f"video{i}"] = videoData

    return render_template('result.html', 
                           URL=URL, 
                           channel_id=channel_id, 
                           channelDetails=channelAbout, 
                           creationDate=creationDate,
                           relVidsIDs=relVidsIDs,
                           relVids=relVidsInfo
                        )
    #"""

    # API disconnected mode: ON
    #channelDetails = (1, 2, 3, 4, 5, 6, 7, 8, 10)
    #return render_template('result.html', URL=URL, channel_id=channel_id, channelDetails=channelDetails, relevantVideos=relVids)

if __name__ == '__main__':
    app.run()



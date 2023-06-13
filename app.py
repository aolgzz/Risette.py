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
from risette_core import get_relevant_vids, get_video_details, get_uploads_id
from risette_core import get_latestvids_dataframe, sort_df_by_duration, sort_df_by_likes, generate_html_link
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
    
    #Generate me dictionary with the three rel vids
    channelAbout = get_channel_details(youtube, get_channel_id(URL))
    creationDate = iso8601_to_prettydate(channelAbout[5])

    relVidsIDs = get_relevant_vids(youtube, channel_id)
    relVidsInfo = {}

    for i, videoID in enumerate(relVidsIDs, start=1):
        videoData = get_video_details(youtube, videoID)
        relVidsInfo[f"video{i}"] = videoData


    #Generate HTML tables
    myDataFrame = get_latestvids_dataframe(youtube, get_uploads_id(youtube, channel_id))

    sortedByDurationDF = sort_df_by_duration(myDataFrame, True, 10)[['Title', 'Video Duration', 'ID']]
    sortedByLikesDF = sort_df_by_likes(myDataFrame, True, 10)[['Title', 'Likes', 'ID']]


    sortedByDurationDF['Title'] = sortedByDurationDF.apply(generate_html_link, axis=1)
    sortedByLikesDF['Title'] = sortedByLikesDF.apply(generate_html_link, axis=1)

    durationTable = sortedByDurationDF.drop('ID', axis=1).to_html(index=False, classes='table table-striped', escape=False)
    likesTable = sortedByLikesDF.drop('ID', axis=1).to_html(index=False, classes='table table-striped', escape=False)

    return render_template('result.html', 
                           URL=URL, 
                           channel_id=channel_id, 
                           channelDetails=channelAbout, 
                           creationDate=creationDate,
                           relVidsIDs=relVidsIDs,
                           relVids=relVidsInfo,
                           htmlTable1=durationTable,
                           htmlTable2=likesTable
                        )
    #"""

    # API disconnected mode: ON
    #channelDetails = (1, 2, 3, 4, 5, 6, 7, 8, 10)
    #return render_template('result.html', URL=URL, channel_id=channel_id, channelDetails=channelDetails, relevantVideos=relVids)

if __name__ == '__main__':
    app.run(debug=True)

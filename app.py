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
    
    return render_template('result.html', URL=URL, channel_id=channel_id, channelDetails=channelAbout, creationDate=creationDate)
    
    #"""

    # API disconnected mode: ON
    #return render_template('result.html', URL=URL, channel_id=channel_id)

if __name__ == '__main__':
    app.run(debug=True)



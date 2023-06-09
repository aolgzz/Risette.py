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
from risette_core import get_channel_id

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/analysisResult", methods=["POST"])
def result():
    URL = request.form["channel_url"]
    #print(URL)

    channel_id = get_channel_id(URL)
    print(channel_id)

    if channel_id == "Error 404":
        error_message = "Error 404. YouTube channel not found"
        return render_template('index.html', error_message=error_message)
    
    return render_template('result.html', URL=URL, channel_id=channel_id)

if __name__ == '__main__':
    app.run()



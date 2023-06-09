#===================================================================#
#                                                                   #
#    A script that validates the URL inserted in the form           #
#    is a YouTube URL based on a regex                              #
#    gatekeeper.py Pre-alpha version                                #
#                                                                   #
#-------------------------------------------------------------------#
#                                                                   #
#    Arturo Olivares                                                #
#                                                                   #
#   Copyright (C) 2023 Arturo Olivares                              #
#   GNU GPLv3                                                       #
#                                                                   #
#===================================================================#

from browser import document, alert
import re

def validate_form_url(event):
    input_value = document.getElementById('searchbar')
    url = input_value.value

    regex = r"https?://(?:www\.)?youtube\.com/(?:@[\w-]+|c/[\w-]+|user/[\w-]+)"

    if not re.match(regex, url):
        alert("""Invalid YouTube channel link. Please try again.

Valid URLs:

- Handle URL (e.g. youtube.com/@youtubecreators)
- Customised URL (e.g. youtube.com/c/YouTubeCreators)
- Legacy username URL (e.g. youtube.com/user/YouTube)
""")
        event.preventDefault()

document.querySelector('form').bind('submit', validate_form_url)


# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import requests
from getPlaylist import Songs


class YoutubeConversion(Songs):
    def __init__(self):
        super().__init__()
        self.specificPlaylistSongDict(5)
        
        
    
    def getYoutubeIDs(self):
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part":"snippet",
            "key":"AIzaSyAAIReGu0D9R8eQf8WMUz-_ohrQ9hkdFE0",
            "q": self.youtubeQuery[1]
        }
        queryRequest = requests.get(url=url, params=params) 
        print(queryRequest.json()['items'][0])



youtube = YoutubeConversion()
youtube.getYoutubeIDs()

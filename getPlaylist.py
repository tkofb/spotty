from dotenv import load_dotenv
import os
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Been using this treeVisualizer to help with JSON objects
from treeVisualizer import visualizeDict 

class SpotipyObject:

    amount = 0
    
    def __init__(self):
        self.requestUserAuthorization()

    def requestUserAuthorization(self):
        load_dotenv()

        self.clientId = os.getenv("CLIENT_ID")
        self.clientSecret = os.getenv("CLIENT_SECRET")
        
        # self.scope = #Add Scope Needed

        self.spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth( 
            scope=self.scope, client_id=self.clientId, client_secret=self.clientSecret, redirect_uri="http://localhost:8888/callback", 
            cache_path='/home/jani/Projects/SpotifyListener/.cache-tkogds@gmail.com'))
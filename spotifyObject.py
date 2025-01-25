from dotenv import load_dotenv
import os
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotipyObject:
    def __init__(self):
        self.requestUserAuthorization()

    def requestUserAuthorization(self):
        load_dotenv()

        self.clientId = os.getenv("CLIENT_ID")
        self.clientSecret = os.getenv("CLIENT_SECRET")

        self.scope = "playlist-read-private playlist-read-collaborative"

        self.spotifyObject = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.scope,
                client_id=self.clientId,
                client_secret=self.clientSecret,
                redirect_uri="http://localhost:8888/callback",
                cache_path= os.getcwd() + ".cache",
            )
        )

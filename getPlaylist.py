import os
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Been using this treeVisualizer to help with JSON objects
from treeVisualizer import visualizeDict 
from spotifyObject import SpotipyObject

class PlaylistDefinition():
    def __init__(self):
        self.sp = SpotipyObject().spotifyObject
        self.testPlaylists = self.sp.current_user_playlists()['items']

    def listPlaylists(self):
        for pos, name in enumerate(self.testPlaylists):
            print(f"{pos+1}. {self.testPlaylists[pos]['name']}")
        
    def assignPlaylistToID(self):
        self.idDict = dict()
        for pos, name in enumerate(self.testPlaylists):
            print(f"{pos+1}. {self.testPlaylists[pos]['id']}")
            self.idDict[pos+1] = self.testPlaylists[pos]['id']
        print(self.idDict)
        
playlist = PlaylistDefinition()
playlist.listPlaylists()
playlist.assignPlaylistToID()
        












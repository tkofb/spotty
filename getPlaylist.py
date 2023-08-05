import os
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Been using this treeVisualizer to help with JSON objects
from treeVisualizer import visualizeDict 
from spotifyObject import SpotipyObject

class Playlists():
    def __init__(self):
        self.sp = SpotipyObject().spotifyObject
        self.testPlaylists = self.sp.current_user_playlists()['items']

    def listPlaylists(self):
        for pos, name in enumerate(self.testPlaylists):
            print(f"{pos+1}. {self.testPlaylists[pos]['name']}")
        
    def assignPlaylistToID(self):
        self.idDict = dict()
        for pos, name in enumerate(self.testPlaylists):
            self.idDict[pos+1] = self.testPlaylists[pos]['id']
            
    def askForPlaylistToDownload(self):
        def askAgain():
            print("INVALID PLAYLIST TRY AGAIN")
            self.askForPlaylistToDownload()
        
        print("Which playlist would you like to download?")
        print("------------------------------------------")
        self.assignPlaylistToID()
        self.listPlaylists()
        print("------------------------------------------")
        self.chosenPlaylist = input("Playlist to Download: ")
        
        try:
            givenValue = int(self.chosenPlaylist)
            if givenValue not in self.idDict:
                askAgain()
        except Exception as e:
            print()
            print(e)
            askAgain()
            
        
            

        
class Songs(Playlists):
    def __init__(self):
        super().__init__()
        
    def getSongs(self):
        pass
    
        
playlist = Playlists()
playlist.askForPlaylistToDownload()












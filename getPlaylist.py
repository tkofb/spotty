import os
import shutil
import json
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotifyObject import SpotipyObject
# Been using this treeVisualizer to help with JSON objects
from treeVisualizer import visualizeDict 

class Playlists():
    def __init__(self):
        self.sp = SpotipyObject().spotifyObject
        self.testPlaylists = self.sp.current_user_playlists()['items']
        self.assignPlaylistToID()
        self.playlistNames = dict()
        self.setPlaylistNames()

    # All File Operations
    
    def makeFolderForPlaylistWithName(self, directoryName):
        os.chdir('MusicDownloads/')
        os.mkdir(directoryName)
        os.chdir('..')
        
    def makeFolderForPlaylistWithNumber(self, playlistNumber):
        os.chdir('MusicDownloads/')
        os.mkdir(self.getPlaylistName(1))
        os.chdir('..')
        
    def removeAllPlaylists(self):
        try:
            currentDirectory = '/home/jani/Projects/SpotifyToMP3/MusicDownloads'
            shutil.rmtree(currentDirectory)
            
            os.mkdir('MusicDownloads/')
        except: os.mkdir('MusicDownloads/')
        
    def deleteSpecificPlaylistWithNumber(self, playlistNumber):
        if playlistNumber not in self.playlistNames: return
        
        playlist = self.getPlaylistName(number=playlistNumber)
        
        os.chdir('MusicDownloads/')
        shutil.rmtree(playlist)
        os.chdir('..')
        
    def deleteSpecificPlaylistWithName(self, playlistName):
        if playlistName not in self.playlistNames.values(): return
        
        for pos,value in enumerate(self.playlistNames.values()):
            if value == playlistName: playlistLocation = pos
        
        self.deleteSpecificPlaylistWithNumber(playlistLocation)
        
    def getPlaylistName(self,number=1):
        return self.playlistNames[number]
        
    def setPlaylistNames(self):
        for pos, name in enumerate(self.testPlaylists):
            self.playlistNames[pos+1] = self.testPlaylists[pos]['name']
    
    def listPlaylists(self):
        for pos, name in enumerate(self.testPlaylists):
            print(f"{pos+1}. {self.testPlaylists[pos]['name']}")
        
    def assignPlaylistToID(self):
        self.idDict = dict()
        for pos, name in enumerate(self.testPlaylists):
            self.idDict[pos+1] = self.testPlaylists[pos]['id']
            
    def askForPlaylistToDownload(self):
        def askAgain():
            print()
            print("INVALID PLAYLIST TRY AGAIN")
            self.askForPlaylistToDownload()
        
        print("Which playlist would you like to download?")
        print("------------------------------------------")
        self.listPlaylists()
        print("------------------------------------------")
        
        try:
            self.chosenPlaylist = int(input("Playlist to Download: "))
            if self.chosenPlaylist not in self.idDict:
                askAgain() 
        except Exception as e:
            askAgain()
            
        
class Songs(Playlists):
    def __init__(self):
        super().__init__()
        
    def songDict(self, hashcode):
        #Spotify API only lets you gain access to 100 songs in a playlist
        self.songs = self.sp.playlist_items(self.idDict[hashcode], limit=100)
        
        self.youtubeQuery = dict()
        
        for i in range(len(self.songs['items'])):
            songName = self.songs['items'][i]['track']['name']
            
            allArtists = " - "
            amountOfArtists = len(self.songs['items'][i]['track']['artists'])
            
            for j in range(amountOfArtists):
                artistName = self.songs['items'][i]['track']['artists'][j]['name']
                
                if j == amountOfArtists - 1: 
                    allArtists += artistName
                    break
                allArtists += f"{artistName}, "
                
            self.youtubeQuery[i+1] = songName + allArtists
            
        return self.youtubeQuery
    
    def specificPlaylistSongDict(self,playlistNumber):
        if type(playlistNumber) != int or playlistNumber not in self.idDict:
            return
        else:
            self.songDict(playlistNumber)
    
    def listSongsRequested(self):
        self.askForPlaylistToDownload()
        self.songs = self.specificPlaylistSongDict(self.chosenPlaylist)
        
        
if __name__ == "__main__":
    songs = Songs()
    playlistName = songs.getPlaylistName(number=2)
    
    songs.makeFolderForPlaylistWithNumber(1)













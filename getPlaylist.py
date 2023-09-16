import os
import shutil
import json
import requests
import spotipy
from math import ceil
from spotipy.oauth2 import SpotifyOAuth
from spotifyObject import SpotipyObject
# Been using this treeVisualizer to help with JSON objects
from treeVisualizer import visualizeDict 

class Playlists():
    def __init__(self):
        self.sp = SpotipyObject().spotifyObject
        self.testPlaylists = self.sp.current_user_playlists()['items']
        self.assignPlaylistToID()
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
        self.playlistNames = dict()
        
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
        
        self.spotifyObjects = []
        self.youtubeQuery = dict()
    
    #Did this because the spotify API surprisingly doesn't have a total length variable
    def playlistLength(self, playlistNumber):
        length = 0
        offset = 0
        
        while True:
            currentPlaylistLength = len(self.sp.playlist_items(self.idDict[playlistNumber],offset=offset)['items'])
            
            if (currentPlaylistLength != 100): 
                length += currentPlaylistLength
                break
            else:
                length += 100
                offset += 100
                
        return length
    
    def createNecessarySpotifyObjects(self, playlistNumber):
        separator = 0
        objectCount = ceil(self.playlistLength(playlistNumber)/100)
        
        for i in range(objectCount):
            currentObject = self.sp.playlist_items(self.idDict[playlistNumber], offset=separator, limit=100)
            self.spotifyObjects.append(currentObject)
            separator += 100
                     
        
    def songDict(self, hashcode):
        #Spotify API only lets you gain access to 100 songs in a playlist
        self.createNecessarySpotifyObjects(hashcode)
        
        songNumber = 1
        
        self.songs = self.sp.playlist_items(self.idDict[hashcode], limit=100)
        
        for spotifyObject in self.spotifyObjects:
                for i in range(len(spotifyObject['items'])):
                    songName = spotifyObject['items'][i]['track']['name']
                    
                    allArtists = " - "
                    
                    #In case the artist is lesser known and doesn't have an established artist page
                    try:
                        amountOfArtists = len(spotifyObject['items'][i]['track']['artists'])
                    except KeyError:
                        amountOfArtists = 0
                        allArtists += spotifyObject['items'][i]['track']['show']['publisher']
                    
                    for j in range(amountOfArtists):
                        artistName = spotifyObject['items'][i]['track']['artists'][j]['name']
                        
                        if j == amountOfArtists - 1: 
                            allArtists += artistName
                            break
                        allArtists += f"{artistName}, "
                        
                    self.youtubeQuery[songNumber] = songName + allArtists
                    songNumber += 1
                    
                
            
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
    
    songs.songDict(2)













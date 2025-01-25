import os
import shutil
import json
import requests
import spotipy
from math import ceil
from spotipy.oauth2 import SpotifyOAuth
from spotifyObject import SpotipyObject

class Playlists():
    def __init__(self):
        self.sp = SpotipyObject().spotifyObject
        self.testPlaylists = self.sp.current_user_playlists()['items']
        self.assignPlaylistToID()
        self.setPlaylistNames()

    # All File Operations
    
    def makeFolderForPlaylistWithName(self, directoryName):
        os.chdir('music/')
        os.mkdir(directoryName)
        os.chdir('..')
        
    def makeFolderForPlaylistWithNumber(self, playlistNumber):
        os.chdir('music/')
        os.mkdir(self.getPlaylistName(playlistNumber))
        os.chdir('..')
        
    def removeAllPlaylists(self):
        try:
            currentDirectory = 'music/'
            shutil.rmtree(currentDirectory)
            
            os.mkdir('music/')
        except: os.mkdir('music/')
        
    def deleteSpecificPlaylistWithNumber(self, playlistNumber):
        if playlistNumber not in self.playlistNames: return
        
        playlist = self.getPlaylistName(number=playlistNumber)
        
        os.chdir('music/')
        shutil.rmtree(playlist)
        os.chdir('..')
        
    def deleteSpecificPlaylistWithName(self, playlistName):
        for entry in os.listdir("./music"):
            if playlistName == entry:
                shutil.rmtree(f"./music/{entry}")
        
    def getPlaylistName(self,number):
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
        
        print("------------------------------------------")
        self.listPlaylists()
        print("------------------------------------------")
        
        try:
            self.chosenPlaylist = int(input("Playlist to Download: "))
            if self.chosenPlaylist not in self.idDict: askAgain() 
            else: print()
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
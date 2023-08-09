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
        self.assignPlaylistToID()
        self.playlistNames = dict()

    def makeFolderForPlaylist(self, directoryName):
        os.chdir('MusicDownloads/')
        os.mkdir(directoryName)
        os.chdir('..')
        
    def listPlaylists(self):
        for pos, name in enumerate(self.testPlaylists):
            print(f"{pos+1}. {self.testPlaylists[pos]['name']}")
            self.playlistNames[pos+1] = self.testPlaylists[pos]['name']
        
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
        #Spotify API only letrs you gain access to 100 songs in a playlist
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
            
            
                
            album = "" if self.songs['items'][i]['track']['album']['album_type'] != 'album' else f" | Album: {self.songs['items'][i]['track']['album']['name']}"
            
                
            self.youtubeQuery[i+1] = songName + allArtists + album
            
        return self.youtubeQuery
    
    def specificPlaylistSongDict(self,playlistNumber):
        if type(playlistNumber) != int or playlistNumber not in self.idDict:
            return
        else:
            self.songDict(playlistNumber)
    
    def listSongsRequested(self):
        self.songs = self.specificPlaylistSongDict(4)
        
        
if __name__ == "__main__":
    songs = Playlists()
    songs.makeFolderForPlaylist('ab')  
    songs.askForPlaylistToDownload()
    print(songs.playlistNames[songs.chosenPlaylist])
    songs.makeFolderForPlaylist('ab')













import os
import json
import requests
from getPlaylist import Songs
from pytube import YouTube
from youtubesearchpython import *
import mutagen
from mutagen.easyid3 import EasyID3

class YoutubeConversion(Songs):
    def __init__(self):
        super().__init__()
        self.askForPlaylistToDownload()
        self.specificPlaylistSongDict(self.chosenPlaylist)
        
        self.getYoutubeURLS()
    
    def getYoutubeURLS(self):
        self.songToYoutube = dict()
        songCount = 0
        
        for songName in self.youtubeQuery.values():
            songList = VideosSearch(songName, limit=1).result()
            
            songCount += 1
            
            if(len(songList['result']) > 0): 
                videoId = songList['result'][0]['id']
            
                youtubeUrl = "https://www.youtube.com/watch?v=" + videoId
            
                self.songToYoutube[songCount] = youtubeUrl
            
                print(f'{songName} found ({songCount}/{len(self.youtubeQuery)})')
            else: 
                print(f'{songName} NOT FOUND ({songCount}/{len(self.youtubeQuery)})')
    
    
    def askForFileName(self):
        name = input("What do you want to name the playlist? ")
        self.fileName = name

    def askForMetadizationFormat(self):
        name = input("Would you like to metadize your music? (Y/N): ")
        
        if(name == 'Y' or name == 'y'): self.metadize = True
        else: self.metadize = False
        
        print()

    
    def downloadAllSongs(self):
        print()
        self.askForFileName()
        self.askForMetadizationFormat()
        
        for songNumber, i in enumerate(self.songToYoutube.values()):
            try:
                currentSong,artist = self.downloadSong(i, self.metadize, songNumber + 1)
                print(f"Song: {currentSong} by {artist} finished downloading ({songNumber+1}/{len(self.youtubeQuery)})")
            except Exception as e:
                print(e)
            
    def downloadSong(self, youtubeLink, metadize, songIndex):
        yt = YouTube(youtubeLink)
        song = yt.title
        artist = yt.author

        audioOnlyStreams = yt.streams.filter(only_audio=True)
        firstStream = audioOnlyStreams[0]

        if '/' in song: song = song.replace('/','')
        if '/' in artist: artist = artist.replace('/','')
        
        songPath = f'MusicDownloads/{self.fileName}'
        
        firstStream.download(output_path = songPath, filename = f'{song}.mp3')
        
        if(metadize): self.metadizeSong(songPath + f'/{song}.mp3', songIndex)
            
        return (song,artist)
    
    def metadizeSong(self, songPath, songNumber):
        try:
            song = EasyID3(songPath)
        except:
            song = mutagen.File(songPath, easy = True)
            song.add_tags()
            
        song['artist'] = None
        song['genre'] = None
        song['playlist'] = self.fileName
        song.save(songPath)
        print(song)
        
        
        
            
        
        
        
         
if __name__ == "__main__":
    youtube = YoutubeConversion()
    youtube.downloadAllSongs()
    
    

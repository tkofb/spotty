import os
import json
import requests
from getPlaylist import Songs
from pytube import YouTube
from youtubesearchpython import *

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
        name = input("Would you like to include the artist name in download format? (Y/N): ")
        
        if(name == 'Y' or name == 'y'): self.metadize = True
        else: self.metadize = False
        
        print()

    
    def downloadAllSongs(self):
        print()
        self.askForFileName()
        self.askForMetadizationFormat()
        
        for songNumber, i in enumerate(self.songToYoutube.values()):
            try:
                currentSong,artist = self.downloadSong(i,self.metadize)
                print(f"Song: {currentSong} by {artist} finished downloading ({songNumber+1}/{len(self.youtubeQuery)})")
            except Exception as e:
                print(e)
            
    def downloadSong(self, youtubeLink, metadize):
        yt = YouTube(youtubeLink)
        song = yt.title
        artist = yt.author

        audioOnlyStreams = yt.streams.filter(only_audio=True)
        firstStream = audioOnlyStreams[0]

        if '/' in song: song = song.replace('/','')
        if '/' in artist: artist = artist.replace('/','')
        
        if(metadize):
            firstStream.download(output_path = f'MusicDownloads/{self.fileName}', filename = f'{song}|-|{artist}.mp3')
        else:
            firstStream.download(output_path = f'MusicDownloads/{self.fileName}', filename = f'{song}.mp3')
        
        return (song,artist) 
         
if __name__ == "__main__":
    youtube = YoutubeConversion()
    youtube.downloadAllSongs()

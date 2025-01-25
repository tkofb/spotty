import os
import json
import requests
from getPlaylist import Songs
from pytube import Search, YouTube
import yt_dlp
import logging
import mutagen
from mutagen.easyid3 import EasyID3
import sys

class YoutubeConversion(Songs):
    def __init__(self):
        super().__init__()
        self.askForPlaylistToDownload()
        self.specificPlaylistSongDict(self.chosenPlaylist)
        self.getYoutubeURLS()
    
    def getYoutubeURLS(self):
        self.songToYoutube = dict()
        songCount = 0
        
        pytube_logger = logging.getLogger('pytube')
        pytube_logger.setLevel(logging.ERROR)
        
        print("Song List:")

        for songName in self.youtubeQuery.values():
            songList = Search(songName)
            
            if(len(songList.results) > 0): 
                videoId = songList.results[0].video_id
            
                youtubeUrl = "https://www.youtube.com/watch?v=" + videoId
            
                self.songToYoutube[songCount] = youtubeUrl
            
                songCount += 1
                print(f'{songName} found ({songCount}/{len(self.youtubeQuery)})')
            else: 
                print(f'{songName} NOT FOUND ({songCount}/{len(self.youtubeQuery)})')
    
    def askForFileName(self):
        name = input("What do you want to name the playlist? ")
        self.fileName = name
        
        if self.fileName == "":
            self.fileName = self.getPlaylistName(self.chosenPlaylist)
        
            
    def downloadAllSongs(self):
        print()
        self.askForFileName()
        
        self.deleteSpecificPlaylistWithName(self.fileName)
        self.makeFolderForPlaylistWithName(self.fileName)

        for songNumber, i in enumerate(self.songToYoutube.values()):
            self.download_audio(i)

    def download_audio(self, link):
        def download_hook(d):
            if d['status'] == 'downloading':
                sys.stdout.write(
                    f"\r[download] {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']} ETA {d['_eta_str']}"
                )
                sys.stdout.flush()
            elif d['status'] == 'finished':
                print(f"\n[download] Completed: {d['filename']}")

        ydl_opts = {
            'quiet': True, 
            'progress_hooks': [download_hook],
            'extract_audio': True,
            'format': 'bestaudio',
            'outtmpl': f'music/{self.fileName}/%(title)s.mp3',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as video:
            video.extract_info(link, download=True)

         
if __name__ == "__main__":
    youtube = YoutubeConversion()
    youtube.downloadAllSongs()
    
    

import os
import json
import requests
from getPlaylist import Songs
from testYoutubeDownload import downloadSong


class YoutubeConversion(Songs):
    def __init__(self):
        super().__init__()
        self.askForPlaylistToDownload()
        self.specificPlaylistSongDict(self.chosenPlaylist)
        
        self.getYoutubeURLS()
        print(self.songToYoutube.values())
        print(self.songToYoutube.keys())
    
    def getYoutubeURLS(self):
        self.songToYoutube = dict()
        songCount = 0
        url = "https://www.googleapis.com/youtube/v3/search"
        
        for songName in self.youtubeQuery.values():
            params = {
                "part":"id",
                "key":"AIzaSyAAIReGu0D9R8eQf8WMUz-_ohrQ9hkdFE0",
                "q": songName
            }
            
            queryRequest = requests.get(url=url, params=params)
            
            if 'error' in queryRequest.json():
                print("Sorry max requests for the day have been reached.")
                break
            
            songCount += 1
            
            videoId = queryRequest.json()['items'][0]['id']['videoId']
            
            youtubeUrl = "https://www.youtube.com/watch?v=" + videoId
            
            self.songToYoutube[songCount] = youtubeUrl
            
    def setFileName(self, name):
        self.fileName = name
    
    def askForFileName(self):
        name = input("What do you want to name the plalist? ")
        self.setFileName(name)
                    
    def downloadYoutubeURL(self):
        self.askForFileName()
        
        for songNumber, i in enumerate(self.songToYoutube.values()):
            downloadSong(i)
            print(f"Song {songNumber + 1} finished downloading")
         
            
            
            
             


if __name__ == "__main__":
    youtube = YoutubeConversion()
    youtube.downloadYoutubeURL()


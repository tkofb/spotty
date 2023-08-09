import os
import json
import requests
from getPlaylist import Songs


class YoutubeConversion(Songs):
    def __init__(self):
        super().__init__()
        self.specificPlaylistSongDict(5)
    
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
            
    def downloadYoutubeURL(self):
        pass
         
            
            
            
             


if __name__ == "__main__":
    youtube = YoutubeConversion()
    youtube.getYoutubeIDs()


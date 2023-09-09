import os
from pytube import YouTube

def downloadSong(youtubeLink):
    yt = YouTube(youtubeLink)

    audioOnlyStreams = yt.streams.filter(only_audio=True)
    firstStream = audioOnlyStreams[0]

    firstStream.download(output_path = f'MusicDownloads/{fileName}', filename = f'{yt.title}.mp3')
    
    return yt.title() 
    
if __name__ == "__main__":
    downloadSong('http://youtube.com/watch?v=2lAe1cqCOXo')
from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

@app.get("/api/video")
def getYouTube(link: str):
    youtubeObject = YouTube(link)
    print(youtubeObject)
    return {
        "audio": youtubeObject.streams.get_audio_only(),
        "video_low": youtubeObject.streams.get_lowest_resolution(),
        "video_high": youtubeObject.streams.get_highest_resolution()
    }

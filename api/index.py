from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.get("/api/audio/{link}")
def getYouTubeAudio(self, link: str):
    youtubeObject = YouTube(link)
    return youtubeObject.streams.get_audio_only()

@app.get("/api/video/{link}")
def getYouTubeVideo(self, link: str):
    youtubeObject = YouTube(link)
    return youtubeObject.streams.get_audio_only()
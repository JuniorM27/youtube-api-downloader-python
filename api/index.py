from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.get("/api/audio")
def getYouTubeAudio(self, link):
    youtubeObject = YouTube(link)
    return youtubeObject.streams.get_audio_only()

@app.get("/api/video")
def getYouTubeVideo(self, link):
    youtubeObject = YouTube(link)
    return youtubeObject.streams.get_audio_only()
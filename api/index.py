from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

@app.get("/api/video/{link}")
def getYouTubeAudio(self, link: str):
    youtubeObject = YouTube(link)
    print(youtubeObject)
    if len(link) == 0:
        return {"error": "Link required!"}
    elif youtubeObject is None:
        return {"error": "Not Found!"}
    else:
        return {
            "audio": youtubeObject.streams.get_audio_only(),
            "video": youtubeObject.streams.get_highest_resolution()
        }
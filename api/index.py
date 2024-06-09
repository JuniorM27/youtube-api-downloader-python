from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from pytube import YouTube
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/info")
def getYouTube(link: str):
    youtubeObject = YouTube(link)

    return {
        "properties": youtubeObject,
        "audio": FileResponse(youtubeObject.streams.get_audio_only(), filename=youtubeObject.title, media_type="application/octet-stream"),
        "video_low": FileResponse(youtubeObject.streams.get_lowest_resolution(), filename=youtubeObject.title, media_type="application/octet-stream"),
        "video_high": FileResponse(youtubeObject.streams.get_highest_resolution(), filename=youtubeObject.title, media_type="application/octet-stream")
    }

@app.get("/api/audio")
def getYouTubeAudio(link: str):
    youtubeObject = YouTube(link)
    audio_stream = youtubeObject.streams.get_audio_only()
    return StreamingResponse(audio_stream, media_type="audio/mp4")

@app.get("/api/video")
def getYouTubeVideo(link: str):
    youtubeObject = YouTube(link)
    video_stream = youtubeObject.streams.get_highest_resolution()
    return StreamingResponse(video_stream, media_type="video/mp4")
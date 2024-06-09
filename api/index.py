from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse, Response
from pytube import YouTube
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def downloadVideo(video_stream):
    video_buffer = io.BytesIO()
    video_stream.stream_to_buffer(video_buffer)
    video_buffer.seek(0)
    video_data = video_buffer.getvalue()

    response = Response(content=video_data, media_type="video/mp4")
    response.headers["Content-Disposition"] = f"attachment; filename=video.mp4"
    return response

def downloadAudio(video_stream):
    video_buffer = io.BytesIO()
    video_stream.stream_to_buffer(video_buffer)
    video_buffer.seek(0)
    video_data = video_buffer.getvalue()

    response = Response(content=video_data, media_type="audio/mp3")
    response.headers["Content-Disposition"] = f"attachment; filename=audio.mp3"
    return response


def stream(video_stream):
        with io.BytesIO() as video_buffer:
            video_stream.stream_to_buffer(video_buffer)
            video_buffer.seek(0)
            while True:
                chunk = video_buffer.read(1024)
                if not chunk:
                    break
                yield chunk

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
    return downloadAudio(audio_stream)


@app.get("/api/video")
def getYouTubeVideo(link: str):
    youtubeObject = YouTube(link)
    video_stream = youtubeObject.streams.get_highest_resolution()
    return downloadVideo(video_stream)

@app.get("/api/stream/video")
def getYouTubeStreamVideo(link: str):
    youtubeObject = YouTube(link)
    video_stream = youtubeObject.streams.get_highest_resolution()
    return StreamingResponse(stream(video_stream), media_type="video/mp4")

@app.get("/api/stream/audio")
def getYouTubeStreamAudio(link: str):
    youtubeObject = YouTube(link)
    video_stream = youtubeObject.streams.get_audio_only()
    return StreamingResponse(stream(video_stream), media_type="video/mp4")

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse, Response
from pytube import YouTube
from fastapi.middleware.cors import CORSMiddleware
import io
from unidecode import unidecode
import uvicorn

app = FastAPI()

uvicorn.Config(app, timeout_keep_alive=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download(video_stream, mediaType, nombre = "audio", extension = "mp3"):
    video_buffer = io.BytesIO()
    video_stream.stream_to_buffer(video_buffer)
    video_buffer.seek(0)
    video_data = video_buffer.getvalue()

    response = Response(content=video_data, media_type=mediaType)

    response.headers["Content-Disposition"] = f"attachment; filename={unidecode(nombre, "replace", "")}.{extension}"
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

@app.get("/api")
def getApiInfo():
    return {
        "/api/info": "Muestra la información de un video proporcionada por la libreria",
        "/api/audio": "Descarga el video en formato mp3",
        "/api/video": "Descarga el video en formato mp4 con la mejor calidad",
        "/api/video_low": "Descarga el video en formato mp4 con la peor calidad",
        "/api/stream/video": "Abre el video en formato de stream en el servidor",
        "/api/stream/audio": "Abre el audio del video en formato de stream en el servidor"
    }

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
    return download(audio_stream, "audio/mp3", nombre=youtubeObject.title, extension = "mp3")

@app.get("/api/video")
def getYouTubeVideo(link: str):
    youtubeObject = YouTube(link)
    video_stream = youtubeObject.streams.get_highest_resolution()
    return download(video_stream, "video/mp4", nombre=youtubeObject.title, extension = "mp4")

@app.get("/api/video_low")
def getYouTubeVideo(link: str):
    youtubeObject = YouTube(link)
    video_stream = youtubeObject.streams.get_lowest_resolution()
    return download(video_stream, "video/mp4", nombre=youtubeObject.title, extension = "mp4")

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

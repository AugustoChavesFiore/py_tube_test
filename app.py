from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pytube import YouTube

app = FastAPI()
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

async def download_music(url: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            return {"status": "failed", "error": "no audio stream found"}

        stream.download(output_path="downloads", filename=f"./{stream.title}.mp3")
        return stream.title
    except Exception as e:
        print(e)
        return {"status": "failed", "error": str(e)}




@app.post ("/api/download")
async def download(req: Request):
    try:
        body = await req.json()
        url = body["url"]
        filename =  ( f"{ await download_music( url ) }.mp3" ).replace(" ", "%20")
        if "error" in filename:
            return { "error": filename["error"] }

        return { "url_download": f"http://localhost:8000/download/{ filename }" } 
        
    except Exception as e:
        print(e)
        return { "error": 'Error al descargar la musica.' }

@app.get("/download/{filename}")
async def download_file(request: Request):
    try:
        filename = request.path_params["filename"]
        return FileResponse(f'./downloads/{filename}', filename = f'{filename}', media_type="audio/mp3") 
    except Exception as e:
        print(e)
        return { "error": 'Error al descargar la musica.' }
    

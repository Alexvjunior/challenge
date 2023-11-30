import os

from fastapi import APIRouter, File, Query, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from api.translator import service

router = APIRouter()

templates_dir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "templates")


@router.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open(os.path.join(templates_dir, "index.html"), "r") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")


@router.post("/translate")
async def translate_audio(
    source_language: str = Query(...),
    target_language: str = Query(...),
    audio_file: UploadFile = File(...)
) -> JSONResponse:

    transcribed_text = service.transcribe_audio(audio_file)
    translated_text = service.translate_text(
        transcribed_text,
        target_language, source_language
    )
    service.convert_text_to_audio(translated_text, target_language)

    return JSONResponse(
        content={"message": translated_text},
        status_code=200
    )


@router.get("/download")
async def download_audio() -> JSONResponse:

    return FileResponse(
        path="audio.mp3",
        filename="audio.mp3",
        media_type='audio/mp3'
    )

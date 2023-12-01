
from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from app.translator import service

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root():
    return service.get_initial_template()


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
async def download_audio():
    return service.download_audio()

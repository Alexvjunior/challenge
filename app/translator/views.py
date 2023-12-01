
from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from app.translator import service

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        return service.get_initial_template()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Erro with Template: {str(e)}"
        )


@router.post("/translate")
async def translate_audio(
    source_language: str = Query(...),
    target_language: str = Query(...),
    audio_file: UploadFile = File(...)
) -> JSONResponse:

    try:
        transcribed_text = service.transcribe_audio(audio_file)
        translated_text = service.translate_text(
            transcribed_text,
            target_language, 
            source_language
        )
        service.convert_text_to_audio_and_save(
            translated_text, target_language
        )

        return JSONResponse(
            content={"message": translated_text},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Erro with translate audio: {str(e)}"
        )


@router.get("/download")
async def download_audio():
    try:
        return service.download_audio()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Erro Download audio: {str(e)}"
        )

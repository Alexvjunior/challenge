
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse

from apps.translator import service

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        return service.get_initial_template()
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Erro with Template: {str(e)}"
        )


@router.post("/translate", summary="Translate audio")
async def translate_audio(
    source_language: str = Query(..., description="Source language code"),
    target_language: str = Query(..., description="Target language code"),
    audio_file: UploadFile = File(..., description="Audio file to translate")
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
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Erro with translate audio: {str(e)}"
        )


@router.get("/download", summary="Download audio")
async def download_audio():
    try:
        return service.download_audio()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Erro Download audio: {str(e)}"
        )

import speech_recognition as sr
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator
from gtts import gTTS
from pydantic import BaseModel, validator
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Union
import os

app = FastAPI()
templates_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "templates")

app.mount("/", StaticFiles(directory=templates_dir, html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return open("templates/index.html", "r").read()


class TranslationRequest(BaseModel):
    source_language: str
    target_language: str
    audio_file: UploadFile

    @validator("audio_file")
    def validate_audio_type(cls, value):
        allowed_extensions = ('.mp3', '.wav')
        if not value.filename.lower().endswith(allowed_extensions):
            raise ValueError(
                "Unsupported audio format. Please send an MP3 or WAV file.")
        return value


@app.post("/translate/")
async def translate_audio(request: TranslationRequest) -> JSONResponse:
    transcribed_text = transcribe_audio(request.audio_file, request.source_language)
    translated_text = translate_text(transcribed_text, request.target_language)
    audio_response = convert_text_to_audio(translated_text)

    return {"translation": translated_text, "audio_response": audio_response}


def transcribe_audio(audio_file: UploadFile, source_language: str) -> Union[str, None]:
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file.file) as source:
            audio_text = recognizer.recognize_google(
                source, language=source_language)
            return audio_text
    except sr.UnknownValueError:
        raise ValueError("Unable to transcribe audio")
    except sr.RequestError as e:
        raise ValueError(
            f"Error in the transcription service request: {str(e)}")


def translate_text(text: str, target_language: str) -> str:
    translation = Translator().translate(text, dest=target_language)
    return translation.text


def convert_text_to_audio(text: str) -> gTTS:
    audio_response = gTTS(text, lang='en')
    return audio_response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

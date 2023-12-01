import os
from typing import Union

import speech_recognition as sr
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from gtts import gTTS
from openai import OpenAI

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

templates_dir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "templates")

client = OpenAI(
    api_key=os.environ.get(os.getenv("OPENAI_API_KEY")),
)


def transcribe_audio(audio_file: UploadFile) -> Union[str, None]:
    try:
        with open("audio.mp3", "wb") as source:
            source.write(audio_file.file.read())
            source.close()
        with open("audio.mp3", "rb") as audio_file:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
    except sr.UnknownValueError:
        raise ValueError("Unable to transcribe audio")
    except sr.RequestError as e:
        raise ValueError(
            f"Error in the transcription service request: {str(e)}")


def translate_text(
        text: str,
        target_language: str,
        source_language: str
) -> str:

    try:
        tradutor = GoogleTranslator(
            source=source_language, target=target_language)
        return tradutor.translate(text)
    except Exception as e:
        raise ValueError(f"Unable to translate audio: {e}")


def convert_text_to_audio(text: str, target_language: str) -> gTTS:
    try:
        audio_response = gTTS(text, lang=target_language)
        audio_response.save("audio.mp3")
    except Exception as e:
        raise ValueError(f"Unable to converte text in audio: {e}")


def download_audio() -> FileResponse:
    file_path = "audio.mp3"

    if not os.path.exists(file_path):
        raise HTTPException(
            detail=f"File at path {file_path} does not exist.",
            status_code=500
        )

    try:
        return __get_audio_file(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in download audio: {str(e)}"
        )


def __get_audio_file(file_path: str) -> FileResponse:
    return FileResponse(
        path=file_path,
        filename=file_path,
        media_type='audio/mp3'
    )


def get_initial_template():
    try:
        with open(os.path.join(templates_dir, "index.html"), "r") as file:
            return file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Erro with Template: {str(e)}"
        )

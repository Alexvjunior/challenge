import os
from pathlib import Path
from typing import Union

from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from fastapi import UploadFile
from fastapi.responses import FileResponse
from gtts import gTTS
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

templates_dir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "templates")

client = OpenAI(
    api_key=os.environ.get(os.getenv("OPENAI_API_KEY")),
)

audio_file_path = (Path(__file__).resolve(
).parent.parent.parent / "audio.mp3").resolve()


def transcribe_audio(audio_file: UploadFile) -> Union[str, None]:
    try:
        __write_file_audio(audio_file)
        with audio_file_path.open("rb") as audio_file:
            return __convert_audio_to_text_api(audio_file)
    except Exception as e:
        raise Exception(
            f"Internal error: {str(e)}"
        )


def __write_file_audio(audio_file: UploadFile) -> None:
    try:
        with audio_file_path.open("wb") as source:
            source.write(audio_file.file.read())
    except Exception as e:
        raise Exception(
            f"Problems for write file audio: {str(e)}"
        )


@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def __convert_audio_to_text_api(audio_file) -> str:
    return client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )


def translate_text(
        text: str,
        target_language: str,
        source_language: str
) -> str:

    try:
        tradutor = GoogleTranslator(
            source=source_language,
            target=target_language
        )
        return tradutor.translate(text)
    except Exception as e:
        raise ValueError(f"Unable to translate audio: {e}")


def convert_text_to_audio_and_save(text: str, target_language: str) -> gTTS:
    try:
        audio_response = gTTS(text, lang=target_language)
        audio_response.save("audio.mp3")
    except Exception as e:
        raise ValueError(f"Unable to converte text in audio: {e}")


def download_audio() -> FileResponse:

    if not audio_file_path.exists():
        raise FileNotFoundError(
            f"File at path {audio_file_path.name} does not exist."
        )

    try:
        return __get_audio_file(audio_file_path)
    except Exception as e:
        raise Exception(
            f"Error in download audio: {str(e)}"
        )


def __get_audio_file(audio_file_path: Path) -> FileResponse:
    return FileResponse(
        path=audio_file_path.as_posix(),
        filename=audio_file_path.name,
        media_type='audio/mp3'
    )


def get_initial_template():
    try:
        with open(os.path.join(templates_dir, "index.html"), "r") as file:
            return file.read()
    except Exception as e:
        raise FileNotFoundError(f"Problems find template {str(e)}")

import speech_recognition as sr
from fastapi import UploadFile
from googletrans import Translator
from gtts import gTTS
from typing import Union


def transcribe_audio(audio_file: UploadFile) -> Union[str, None]:
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file.file) as source:
            audio_text = recognizer.recognize_google(source, language='en-US')
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

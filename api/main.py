import speech_recognition as sr
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator
from gtts import gTTS
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from typing import Union
import os
from deep_translator import GoogleTranslator
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = FastAPI()


templates_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "templates")

# app.mount("/static", StaticFiles(directory=os.path.join(templates_dir, "static")), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return open(f"{templates_dir}/index.html", "r").read()



@app.post("/translate")
async def translate_audio(
    source_language: str = Query(...), 
    target_language: str = Query(...), 
    audio_file: UploadFile = File(...)
    ) -> JSONResponse:

    transcribed_text = transcribe_audio(audio_file)
    translated_text = translate_text(transcribed_text, target_language, source_language)
    convert_text_to_audio(translated_text, target_language)


    return JSONResponse(content={"translation":translated_text}, status_code=200)

@app.get("/download")
async def translate_audio() -> JSONResponse:

    return FileResponse(path="audio.mp3", filename="audio.mp3", media_type='audio/mp3')


def transcribe_audio(audio_file: UploadFile) -> Union[str, None]:

    try:
        with open("audio.mp3", "wb") as source:
            source.write(audio_file.file.read())
            source.close()                          
        with open("audio.mp3", "rb") as audio_file:
            return client.audio.transcriptions.create(
                    model="whisper-1", 
                    file= audio_file,
                    response_format="text"
                )
    except sr.UnknownValueError:
        raise ValueError("Unable to transcribe audio")
    except sr.RequestError as e:
        raise ValueError(
            f"Error in the transcription service request: {str(e)}")


def translate_text(text: str, target_language: str, source_language:str) -> str:
    tradutor = GoogleTranslator(source= source_language, target=target_language)
    return tradutor.translate(text)


def convert_text_to_audio(text: str, target_language:str) -> gTTS:
    audio_response = gTTS(text, lang=target_language)
    audio_response.save("audio.mp3")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

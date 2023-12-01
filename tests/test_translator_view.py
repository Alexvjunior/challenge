from unittest import mock

from fastapi.responses import Response
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main_success():
    response = client.get("/")
    assert response.status_code == 200


def test_read_main_template_not_found():
    with mock.patch('app.translator.service.get_initial_template', side_effect=FileNotFoundError("Template not Found")):
        response = client.get("/")
        assert response.status_code == 404


def test_translate_audio_not_send_file():

    source_language = "en"
    target_language = "es"

    response = client.post(
        f"/translate?source_language={source_language}&target_language={target_language}",
    )
    assert response.status_code == 422
    assert response.text == '{"detail":[{"type":"missing","loc":["body","audio_file"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.5/v/missing"}]}'


def test_translate_audio_not_allowed():

    response = client.get(
        f"/translate",
    )
    assert response.status_code == 405
    assert response.text == '{"detail":"Method Not Allowed"}'


def test_download_audio_not_allowed():

    url = f"/download"

    response = client.post(f"/download")

    assert response.status_code == 405
    assert response.text == '{"detail":"Method Not Allowed"}'


def test_download_audio_file_not_found():
    with mock.patch('os.path.exists', return_value=False):
        response = client.get(f"/download")
        assert response.status_code == 500
        assert response.json() == {
            'detail': 'File at path audio.mp3 does not exist.'
        }


def test_download_audio_success():

    with mock.patch('app.translator.service.download_audio') as mock_file_response:
        mock_file_response.return_value = Response(
            content="Mocked File Response", status_code=200)
        response = client.get("/download")
        assert response.status_code == 200
        assert response.content == b"Mocked File Response"


def test_download_audio_raises_exception():

    with mock.patch('os.path.exists', return_value=True):
        with mock.patch('app.translator.service.__get_audio_file', side_effect=Exception("File at path audio.mp3 does not exist.")):
            response = client.get("/download")
            assert response.status_code == 500
            assert response.json() == {
                'detail': 'Error in download audio: File at path audio.mp3 does not exist.'
            }

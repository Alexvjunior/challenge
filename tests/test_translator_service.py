from unittest import mock
from unittest.mock import mock_open

import pytest

from app.translator import service


def test_transcribe_audio_exception_write_audio():

    with mock.patch(
        'app.translator.service.__write_file_audio',
        side_effect=Exception("Problems for write file audio")
    ):
        with pytest.raises(
            Exception,
            match="Internal error: Problems for write file audio"
        ):
            service.transcribe_audio(None)


def test_transcribe_audio_exception_convert_audio_to_text_api():
    with mock.patch('app.translator.service.__write_file_audio', return_value=None):
        with mock.patch("pathlib.Path.open", mock_open(read_data=b'')):
            with mock.patch('app.translator.service.__convert_audio_to_text_api', side_effect=Exception("Problems for conect to API")):
                with pytest.raises(Exception) as exc_info:
                    service.transcribe_audio(b'')
    assert str(exc_info.value) == "Internal error: Problems for conect to API"


def test_transcribe_audio_success():
    with mock.patch('app.translator.service.__write_file_audio', return_value=None):
        with mock.patch("pathlib.Path.open", mock_open(read_data=b'')):
            with mock.patch('app.translator.service.__convert_audio_to_text_api', return_value="test"):
                assert service.transcribe_audio(b'') == "test"


def test_translate_text_success():
    result = service.translate_text(
        "Car",
        source_language="en",
        target_language="pt"
    )

    assert result == "Carro"


def test_translate_text_exception():
    with pytest.raises(ValueError) as exc_info:
        service.convert_text_to_audio_and_save(None, "en")

    assert str(
        exc_info.value) == "Unable to converte text in audio: No text to speak"


def test_download_audio_exception_not_exists_file():
    with mock.patch('pathlib.Path.exists', return_value=False):
        with pytest.raises(Exception) as exc_info:
            service.download_audio()

    assert str(exc_info.value) == "File at path audio.mp3 does not exist."


def test_download_audio_exception_get_audio_file():
    with mock.patch('pathlib.Path.exists', return_value=True):
        with mock.patch('app.translator.service.__get_audio_file', side_effect=Exception("File at path audio.mp3 does not exist.")):
            with pytest.raises(Exception) as exc_info:
                service.download_audio()

    assert str(
        exc_info.value) == "Error in download audio: File at path audio.mp3 does not exist."


def test_get_template_exception_not_fount():
    with mock.patch('app.translator.service.get_initial_template', side_effect=Exception("Template not Found")):
        with pytest.raises(Exception) as exc_info:
            service.get_initial_template()

    assert str(
        exc_info.value) == "Template not Found"

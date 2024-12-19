import pytest
from src.fileHandlers.AudioWAVFileProcessor import AudioWAVFileProcessor


@pytest.fixture
def audio_wav_file_processor():
    return AudioWAVFileProcessor()
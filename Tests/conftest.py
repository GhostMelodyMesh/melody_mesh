import pytest
from src.fileHandlers.AudioFileHandler import AudioFileHandler


@pytest.fixture(scope='session')
def sample_test_files_path():
    return ["./rawData/file0.mp3", "./rawData/file1.wav", "./rawData/file2.wav", "./rawData/file3.wav", "./rawData/file4.wav"]


@pytest.fixture(scope='session')
def audio_file_handler():
    return AudioFileHandler()

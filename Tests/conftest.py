import pytest
from src.fileHandlers.AudioFileHandler import AudioFileHandler


@pytest.fixture
def sample_test_files():
    return ["test1", "test2", "test3"]


@pytest.fixture
def audio_file_handler():
    return AudioFileHandler()

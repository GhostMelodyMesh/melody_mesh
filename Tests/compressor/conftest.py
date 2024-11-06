import pytest
from src.compressors.CompressorWAVTeamName import CompressorWAVTeamName


@pytest.fixture
def compressor():
    return CompressorWAVTeamName()

import pytest
from src.compressors.CompressorWAVBaseline import CompressorWAVBaseline


@pytest.fixture(scope='session')
def compressor():
    return CompressorWAVBaseline()

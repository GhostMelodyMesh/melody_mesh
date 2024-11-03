import pytest
from src.compressors.Compressor import CompressorTeamName


def test_compress():
    compressor = CompressorTeamName()
    with pytest.raises(NotImplementedError):
        compressor.compress("test")


def test_group_redundancies():
    compressor = CompressorTeamName()
    with pytest.raises(NotImplementedError):
        compressor.group_redundancies("test")

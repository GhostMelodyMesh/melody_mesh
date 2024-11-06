import pytest
import os.path
import numpy as np
from src.dataTypes.AudioWAV import AudioWAV


PATH = './rawData/'


@pytest.fixture(scope='module')
def compressed_files(compressor, sample_test_files, audio_file_handler) -> dict[str, str: AudioWAV, str: dict[int, AudioWAV]]:
    """
    Fixtures that returns compressed files with sample rates

    :returns: dict with file_name as key and properties original: AudioWAV, compressed: dict[int, AudioWAV]
        Dict[str, {'original': AudioWAV, 'compressed': Dict[int, AudioWAV]}]

    Example structure:
    {
        'file1': {
            'original': AudioWAV_object,
            'compressed': {
                22050: AudioWAV_object,
                11025: AudioWAV_object,
                8000: AudioWAV_object,
                ...
            }
        },
        'file2': {
            ...
        }
    }
    """
    sample_rates = [22050, 11025, 8000, 4000, 2400, 1200]
    result = {}

    for file_name in sample_test_files:
        file_path = f'./{PATH}/{file_name}.wav'
        if not os.path.exists(file_path):
            continue
        original_audio = audio_file_handler.read_as_wav(file_path)
        result[file_name] = {
            'original': original_audio,
            'compressed': {}
        }

        for sample_rate in sample_rates:
            compressed_audio = compressor.lower_quality(original_audio, sample_rate)
            result[file_name]['compressed'][sample_rate] = compressed_audio

    return result

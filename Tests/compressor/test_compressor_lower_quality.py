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


def helper_values_range(original_audio, compressed_audio, sample_rate, rms_tolerance):
    assert np.all(compressed_audio >= -1.0), f"Compressed audio contains values below -1.0 for sample_rate {sample_rate}"
    assert np.all(compressed_audio <= 1.0), f"Compressed audio contains values above 1.0 for sample_rate {sample_rate}"

    # Test if RMS value is within tolerance
    original_rms = np.sqrt(np.mean(np.square(original_audio)))
    compressed_rms = np.sqrt(np.mean(np.square(compressed_audio)))
    assert abs(
        original_rms - compressed_rms) < rms_tolerance, \
        f"RMS value changed significantly after compression to {sample_rate}Hz, original: {original_rms}, compressed: {compressed_rms}"

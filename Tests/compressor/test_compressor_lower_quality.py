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


def test_lower_quality_properties(compressed_files):
    """Test if sample rate is correct and length is scaled properly after compression"""
    for file, data in compressed_files.items():
        original = data['original']
        for sample_rate in data['compressed']:
            compressed = data['compressed'][sample_rate]

            compression_rate = original.sample_rate / sample_rate

            assert compressed.sample_rate == sample_rate, f"Incorrect sample rate after compression to {sample_rate}Hz, current: {compressed.sample_rate}"
            assert len(compressed.audio) == pytest.approx(len(original.audio) / compression_rate, abs=5), \
                f"Incorrect length after compression to {sample_rate}Hz, current: {len(compressed.audio)}"


@pytest.mark.parametrize('sample_rate,rms_tolerance', [
    # (sample_rate, rms_tolerance)
    (22050, 0.05),
    (11025, 0.08),
    (8000, 0.1),
    (4000, 0.15),
    (2400, 0.2),
    (1200, 0.3)
])
def test_lower_quality_values_range(compressor, compressed_files, sample_rate, rms_tolerance):
    """Test if audio values stay in correct range after compression"""
    for file, data in compressed_files.items():
        original = data['original']
        compressed = data['compressed'][sample_rate]
        helper_values_range(original.audio, compressed.audio, sample_rate, rms_tolerance)


@pytest.mark.parametrize('compression_stages, rms_tolerance, length_tolerance', [
    ([22050, 11025], [0.05, 0.08], 10),  # 2-step compression
    ([22050, 11025, 8000], [0.05, 0.08, 0.1], 15),  # 3-step compression
    ([22050, 11025, 8000, 4000], [0.05, 0.08, 0.1, 0.15], 20)  # 4-step compression
])
def test_lower_quality_cascading(compressor, compressed_files, compression_stages, rms_tolerance, length_tolerance):
    """Test cascading compression (multiple quality reductions)"""
    for file, data in compressed_files.items():
        original = data['original']

        compressed = original
        total_compression_rate = 1

        for rate, rms in zip(compression_stages, rms_tolerance):
            compressed = compressor.lower_quality(compressed, rate)
            assert compressed.sample_rate == rate, f"Incorrect sample rate after compression to {rate}Hz"
            helper_values_range(original.audio, compressed.audio, rate, rms)
            total_compression_rate *= (original.sample_rate / rate)

        # Check if final length is within tolerance
        expected_length = len(original.audio) / total_compression_rate
        assert len(compressed.audio) == pytest.approx(expected_length, abs=length_tolerance), \
            f"Unexpected length after cascading compression to {compression_stages}, got {len(compressed.audio)}, expected {expected_length} +- {length_tolerance}"


@pytest.mark.parametrize('invalid_sample_rate', [0, -44100, -1, 100000])
def test_lower_quality_invalid_sample_rate(compressor, sample_test_files, audio_file_handler, invalid_sample_rate):
    """Test handling of invalid sample rates"""
    filepath = f'./{PATH}/{sample_test_files[0]}.wav'
    audio = audio_file_handler.read_as_wav(filepath)

    with pytest.raises(ValueError):
        compressor.lower_quality(audio, invalid_sample_rate)


# TODO zrobić printowanie na ile dobra jest kompresja, zapytać claude jak to zrobić.
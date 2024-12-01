import pytest
import os
import numpy as np
from typing import Dict
from scipy.io import wavfile
from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.AudioWAVFileProcessor import AudioWAVFileProcessor


@pytest.fixture
def processor() -> AudioWAVFileProcessor:
    return AudioWAVFileProcessor()


@pytest.fixture
def sample_audio_data() -> Dict[str, AudioWAV]:
    """ Create sample audio data for testing """
    sample_rate: int = 44100
    duration: float = 1  # seconds
    t: np.ndarray = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    single_channel: np.ndarray = (np.sin(2 * np.pi * 440 * t) * 0.5).astype(np.float32)
    stereo_channel: np.ndarray = np.column_stack([
        np.sin(2 * np.pi * 440 * t) * 0.5,
        np.sin(2 * np.pi * 880 * t) * 0.5
    ]).astype(np.float32)

    return {
        'single_channel': AudioWAV(
            audio=single_channel.reshape(-1, 1),
            format="wav",
            sample_rate=sample_rate,
            n_samples=len(single_channel),
            n_channels=1
        ),
        'stereo_channel': AudioWAV(
            audio=stereo_channel,
            format="wav",
            sample_rate=sample_rate,
            n_samples=len(stereo_channel),
            n_channels=2
        )
    }


def test_write_file_existence(
        processor: AudioWAVFileProcessor,
        sample_audio_data: Dict[str, AudioWAV],
        tmp_path: str
) -> None:
    """ Test that the file is actually created when writing """
    for channel_type, audio_obj in sample_audio_data.items():
        output_file: str = os.path.join(tmp_path, f"{channel_type}_output.wav")

        # Write the file
        processor.write(audio_obj, output_file)

        # Check that the file exists
        assert os.path.exists(output_file), f"File {output_file} was not created"

        # Additional checks
        assert os.path.isfile(output_file), f"{output_file} is not a regular file"
        assert os.path.getsize(output_file) > 0, f"{output_file} is empty"


def test_write_raises_on_nonexistent_directory(
        processor: AudioWAVFileProcessor,
        sample_audio_data: Dict[str, AudioWAV],
        tmp_path: str
) -> None:
    """ Enhanced test for writing to non-existent directory """
    # Create a deeply nested non-existent path
    invalid_path: str = os.path.join(tmp_path, "non_existent_dir1", "non_existent_dir2", "output.wav")

    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        processor.write(sample_audio_data['single_channel'], invalid_path)

    # Verify that no partial file was created
    assert not os.path.exists(os.path.dirname(invalid_path)), "Unexpected directory creation"


def test_read_file_existence(
        processor: AudioWAVFileProcessor,
        tmp_path: str
) -> None:
    """ Test reading a file that definitely exists """
    file_path: str = os.path.join(tmp_path, "test_existing.wav")

    # Create a test wav file (1D array for mono audio)
    sample_rate: int = 44100
    audio: np.ndarray = np.random.randint(-32768, 32767, sample_rate, dtype=np.int16)
    wavfile.write(file_path, sample_rate, audio)

    # Verify file exists before reading
    assert os.path.exists(file_path), "Test file was not created"

    # Try to read the file
    audio_wav: AudioWAV = processor.read(file_path)

    assert isinstance(audio_wav, AudioWAV), "Failed to read existing file"
    assert audio_wav.sample_rate == sample_rate
    assert audio_wav.n_samples == len(audio)
    assert audio_wav.n_channels == 1
    np.testing.assert_almost_equal(audio_wav.audio.flatten(), audio / 2**15, decimal=5)


def test_write_and_read_back(
        processor: AudioWAVFileProcessor,
        sample_audio_data: Dict[str, AudioWAV],
        tmp_path: str
) -> None:
    """ Test writing AudioWAV objects and reading them back """
    for channel_type, audio_obj in sample_audio_data.items():
        output_file: str = os.path.join(tmp_path, f"{channel_type}_output.wav")
        processor.write(audio_obj, output_file)

        # Read the written file
        read_audio: AudioWAV = processor.read(output_file)

        assert isinstance(read_audio, AudioWAV)
        np.testing.assert_almost_equal(read_audio.audio, audio_obj.audio, decimal=5)
        assert read_audio.sample_rate == audio_obj.sample_rate
        assert read_audio.n_samples == audio_obj.n_samples
        assert read_audio.n_channels == audio_obj.n_channels


@pytest.fixture(autouse=True)
def cleanup_tmp_files(tmp_path: str) -> None:
    """ Automatically remove temporary files after each test """
    yield
    for filename in os.listdir(tmp_path):
        file_path: str = os.path.join(tmp_path, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

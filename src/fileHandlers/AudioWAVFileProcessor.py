from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.FileProcessorAbstract import FileProcessorAbstract
from scipy.io import wavfile
import numpy as np
from src.utilities.get_extension import get_extension


class AudioWAVFileProcessor(FileProcessorAbstract):
    def __init__(self):
        pass

    def read(self, file_path: str):
        """ Read an audio file as a .wav file with normalized audio data in range (-1, 1) of type float32 """
        sample_rate, audio = wavfile.read(file_path)
        data_number_type = audio.dtype

        # Normalize audio data based on its type
        match data_number_type:
            case 'float32':
                audio = audio
            case 'int32':
                audio = audio / 2 ** 31
            case 'int16':
                audio = audio / 2 ** 15
            case 'uint8':
                audio = (audio - 128) / 128
            case _:
                raise ValueError("Data type not supported")

        audio = audio.astype(np.float32)

        # Ensure audio data is 2D: mono becomes (n_samples, 1)
        if audio.ndim == 1:
            audio = audio[:, np.newaxis]

        n_samples, n_channels = audio.shape

        return AudioWAV(audio=audio, format='wav', sample_rate=sample_rate, n_samples=n_samples, n_channels=n_channels)

    def write(self, audio: AudioWAV, file_path: str):
        """ Write an Audio object to a file, file_path must include the file extension """
        match get_extension(file_path):
            case "wav":
                wavfile.write(file_path, audio.sample_rate, audio.audio)
            case _:
                raise ValueError("File format not supported")
            